import z from "zod";
import { config } from "dotenv";
config();

const envSchema = z.object({
  NODE_ENV: z
    .enum(["development", "production", "test"])
    .default("development"),
  DATABASE_URL: z.string().trim().min(1),
  UPSTASH_TOKEN: z.string().trim().min(1),
});

export const env = envSchema.parse(process.env);
