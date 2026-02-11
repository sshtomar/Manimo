#!/bin/bash
set -e

VID="/Users/explorer/Manimo/manim_visualizations/media/videos/test_scene/480p15"
OUT="/Users/explorer/Manimo/manim_visualizations/media/comparison"
mkdir -p "$OUT"

ffmpeg -y \
  -i "$VID/classic.mp4" \
  -i "$VID/dark_slate.mp4" \
  -i "$VID/light.mp4" \
  -i "$VID/warm.mp4" \
  -i "$VID/chalkboard.mp4" \
  -i "$VID/whiteboard.mp4" \
  -i "$VID/high_contrast.mp4" \
  -i "$VID/lecture_hall.mp4" \
  -i "$VID/pastel.mp4" \
  -filter_complex "
    [0:v]drawtext=text='classic':fontsize=18:fontcolor=white:borderw=2:bordercolor=black:x=10:y=10[v0];
    [1:v]drawtext=text='dark_slate':fontsize=18:fontcolor=white:borderw=2:bordercolor=black:x=10:y=10[v1];
    [2:v]drawtext=text='light':fontsize=18:fontcolor=black:borderw=2:bordercolor=white:x=10:y=10[v2];
    [3:v]drawtext=text='warm':fontsize=18:fontcolor=white:borderw=2:bordercolor=black:x=10:y=10[v3];
    [4:v]drawtext=text='chalkboard':fontsize=18:fontcolor=white:borderw=2:bordercolor=black:x=10:y=10[v4];
    [5:v]drawtext=text='whiteboard':fontsize=18:fontcolor=black:borderw=2:bordercolor=white:x=10:y=10[v5];
    [6:v]drawtext=text='high_contrast':fontsize=18:fontcolor=white:borderw=2:bordercolor=black:x=10:y=10[v6];
    [7:v]drawtext=text='lecture_hall':fontsize=18:fontcolor=white:borderw=2:bordercolor=black:x=10:y=10[v7];
    [8:v]drawtext=text='pastel':fontsize=18:fontcolor=white:borderw=2:bordercolor=black:x=10:y=10[v8];
    [v0][v1][v2][v3][v4][v5][v6][v7][v8]xstack=inputs=9:layout=0_0|w0_0|w0+w1_0|0_h0|w0_h0|w0+w1_h0|0_h0+h1|w0_h0+h1|w0+w1_h0+h1[out]
  " \
  -map "[out]" \
  -c:v libx264 -crf 18 -preset fast \
  "$OUT/all_themes_grid.mp4"

echo "Grid video saved to: $OUT/all_themes_grid.mp4"
