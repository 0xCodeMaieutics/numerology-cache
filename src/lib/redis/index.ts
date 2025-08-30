import { Redis } from "@upstash/redis";
import { env } from "../../env.ts";
const UPSTASH_URL = "https://sensible-llama-52290.upstash.io";

export const redis = new Redis({
  url: UPSTASH_URL,
  token: env.UPSTASH_TOKEN,
});
