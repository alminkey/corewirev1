import { z } from "zod";

export const pipelineRunType = z.enum([
  "ingest",
  "extract",
  "analyze",
  "draft",
  "publish",
]);

