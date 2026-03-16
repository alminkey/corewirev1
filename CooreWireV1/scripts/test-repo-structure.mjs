import { access } from "node:fs/promises";
import path from "node:path";

const requiredDirs = ["apps/web", "apps/api", "apps/workers"];

const missingDirs = [];

for (const dir of requiredDirs) {
  try {
    await access(path.resolve(dir));
  } catch {
    missingDirs.push(dir);
  }
}

if (missingDirs.length > 0) {
  console.error(`Missing required directories: ${missingDirs.join(", ")}`);
  process.exit(1);
}

console.log("Repository structure smoke check passed.");
