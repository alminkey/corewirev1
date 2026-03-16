import { z } from "zod";

export const articleStatus = z.enum([
  "published",
  "developing_story",
  "retracted",
  "superseded",
]);

export const articleConfidence = z.enum(["low", "medium", "high"]);

