# SWIM

## Swimming Biomechanical Data Format

**SWIM** is an open, extensible data format for storing swimming race, athlete, and biomechanical data.

SWIM provides a common structure for combining data from race timing, video analysis, motion capture, inertial sensors, force measurements, and other swimming-performance systems.

- [Get Started](getting-started.md)
- [Specification](format/specification.md)

---

## Why SWIM?

Swimming data is often collected using multiple systems, each with its own file format, metadata structure, units, and conventions.

SWIM provides a common container for these data.

```text
Race timing ─────┐
Video ───────────┤
Motion capture ──┤
IMU ─────────────┼──→  .swim  ──→  Analysis
Force sensors ───┤
Stroke analysis ─┘