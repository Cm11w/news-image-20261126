// news-image-20261126 — "The World in One Day": a front page summing up
// Thursday 26 November 2026 in one image. The image is the entry.png
// beside this file (drawn procedurally with PIL by draw.py from 29
// verified stories of 26 Nov 2026, following the layout of the 22 Nov
// rank-1 entry); the program copies it to /output/entry.png. No network,
// no randomness, no clock — every run writes the same bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, rmSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, "entry.png");

// Remove only the artifact this program writes (never the whole folder:
// rmSync on the output directory fails with EBUSY on the grader's mount).
rmSync(outPath, { force: true });
copyFileSync(new URL("./entry.png", import.meta.url), outPath);

// Fail loudly instead of submitting a bad file: the gate reads the entry
// as a PNG by its first bytes, so verify the PNG signature after the copy.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!readFileSync(outPath).subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error("entry.png is not a valid PNG");
}
