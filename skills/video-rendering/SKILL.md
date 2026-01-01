---
name: video-rendering
description: "Video rendering optimization, quality settings, and format best practices."
---

<skill_content>

<overview>
Video rendering requires balancing quality, file size, and rendering time. This skill ensures videos are optimized for their intended use case.
</overview>

<mandatory_requirements>

<requirement priority="high">
  <name>Quality Settings Documentation</name>
  <description>MUST document quality settings and rendering parameters with RATIONALE comments</description>
  <rationale>Different use cases require different quality settings. Documentation helps future creators choose appropriate settings.</rationale>
  <consequence>Rendering settings are unclear, hard to optimize for specific use cases</consequence>
</requirement>

<requirement priority="high">
  <name>Appropriate Resolution</name>
  <description>MUST use appropriate resolution for the use case: low for previews, high for final videos</description>
  <rationale>Higher resolution increases rendering time and file size. Use the minimum resolution needed for the use case.</rationale>
  <consequence>Unnecessary rendering time, large file sizes, or poor quality output</consequence>
</requirement>

<requirement priority="medium">
  <name>Frame Rate Considerations</name>
  <description>MUST consider frame rate: 30fps for most cases, 60fps for smooth motion, 24fps for cinematic feel</description>
  <rationale>Frame rate affects smoothness and file size. Choose based on animation needs.</rationale>
  <consequence>Animations look choppy or files are unnecessarily large</consequence>
</requirement>

</mandatory_requirements>

<quality_levels>

<level name="low">
  <description>For quick previews and testing</description>
  <settings>
    - Resolution: 480p (854x480)
    - Frame rate: 15fps
    - Use: Fast iteration, testing animations
  </settings>
</level>

<level name="medium">
  <description>For standard educational videos</description>
  <settings>
    - Resolution: 720p (1280x720)
    - Frame rate: 30fps
    - Use: Most educational content, web sharing
  </settings>
</level>

<level name="high">
  <description>For high-quality presentations</description>
  <settings>
    - Resolution: 1080p (1920x1080)
    - Frame rate: 30fps or 60fps
    - Use: Professional presentations, YouTube
  </settings>
</level>

<level name="production">
  <description>For highest quality output</description>
  <settings>
    - Resolution: 4K (3840x2160) or higher
    - Frame rate: 60fps
    - Use: Professional productions, high-end presentations
  </settings>
</level>

</quality_levels>

</skill_content>

