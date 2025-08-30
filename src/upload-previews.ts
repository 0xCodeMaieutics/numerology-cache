#!/usr/bin/env node

import { randomBytes } from "crypto";
import { redis } from "./lib/redis/index.ts";
import { redisKey } from "./lib/redis/keys.ts";
import { cacheManager } from "./utils/cache/cache-manager.ts";
import { input } from "./utils/input.ts";
import "colors";

const category = await input(`Category:`);

if (!category) {
  console.log("Category usage cancelled.");
  process.exit(0);
}
let batch: number | string = await input(`Batch:`);
try {
  batch = parseInt(batch);
  if (isNaN(batch)) {
    console.log("Batch usage cancelled.");
    process.exit(0);
  }
} catch (error) {
  console.log("Batch usage cancelled.");
  process.exit(0);
}

const previewJson = cacheManager.previews.wikipedia.readPreview(
  batch as number
);

const modifiedPreview = previewJson.map((item, index) => ({
  id: randomBytes(16).toString("hex"),
  ...item,
}));

const key = redisKey.celebrities(null).category(category);
let allCelebs = [];
try {
  allCelebs = (await redis.get<any[]>(key)) ?? [];
} catch (error) {
  allCelebs = [];
}

const result = await redis.set(key, [...allCelebs, ...modifiedPreview]);
console.log("Redis set result:", result);
