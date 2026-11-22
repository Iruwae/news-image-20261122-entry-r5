// news-image-20261122 entry r5 (Node 22, standard library only).
// The entry is the entry.png beside this file; the program copies it to
// /output/entry.png. The gate takes a whole PNG of at most 1 MiB and
// 1024 by 1024 pixels, and the judge sees exactly the bytes copied.
// Built for the make.fun news-image-20261122 bounty: one broadsheet
// image, 35 stories from Sunday 22 November 2026, drawn by draw.py.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const dest = join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), dest);
