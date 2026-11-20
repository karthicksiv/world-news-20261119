// Entry point for the news-image bounty (Node 22, standard library only).
//
// The page itself is entry.png beside this file — a 1024x1024 PNG drawn offline by tools/gen.py
// and rendered with tools/shot.js. The grader runs this file twice in a fresh container with no
// network; all it has to do is place the same bytes at /output/entry.png each time. Copying a
// fixed file is deterministic by construction, so both runs write identical bytes.
//
// MAKEFUN_OUTPUT_DIR stands in for /output outside the grader:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const target = join(process.env.MAKEFUN_OUTPUT_DIR ?? "/output", "entry.png");
copyFileSync(join(here, "entry.png"), target);
