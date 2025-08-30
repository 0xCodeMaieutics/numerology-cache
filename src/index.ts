#!/usr/bin/env node
import "colors";
import { randomBytes } from "crypto";
import {
  calculateLifePath,
  calculateThePsychicNumber,
} from "./utils/number.ts";
import { formatDate } from "date-fns";
import { redis } from "./lib/redis/index.ts";
import { redisKey } from "./lib/redis/keys.ts";

const createCelebrity = async ({
  dob,
  name,
  description,
}: {
  dob: string;
  name: string;
  description?: string;
}) => {
  const dobValue = dob.split("=")[1];
  const nameValue = name.split("=")[1];
  const descriptionValue = description?.split("=")?.[1] ?? "";
  const split = dobValue.split(".");

  let day = split[0];
  let month = split[1];
  let year = split[2];
  const celebId = randomBytes(16).toString("hex");
  const lifePathNumber = calculateLifePath(day, month, year);
  const psychicNumber = calculateThePsychicNumber(parseInt(day));

  const createdAt = new Date().toISOString();
  const index =
    (await redis.rpush(redisKey.celebrities(null).all, {
      id: celebId,
      name: nameValue,
      lifePathNumber: lifePathNumber,
      psychicNumber: psychicNumber,
      dob: dobValue,
      createdAt: createdAt,
      image: "",
      formattedDob: formatDate(new Date(dobValue), "dd LLLL yyyy"),
      ...(descriptionValue ? { description: descriptionValue } : {}),
    })) - 1;
  await redis.set(redisKey.celebrities(celebId).celebIdIndex, index);
};

const dob = process.argv.find((arg) => arg.startsWith("--dob="));
const name = process.argv.find((arg) => arg.startsWith("--name="));
const description = process.argv.find((arg) =>
  arg.startsWith("--description=")
);

if (dob && name) {
  createCelebrity({
    dob,
    name,
    description,
  });
}
