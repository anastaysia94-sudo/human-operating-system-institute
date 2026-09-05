# HOSI Android Client — Starter Architecture

Recommended direction: Kotlin + Jetpack Compose, with the web curriculum remaining the canonical content source.

## Screens

- Home
- Colleges
- Course Catalog
- Lesson Reader
- Research Library
- Atlas
- Progress
- Settings / Privacy

## Boundaries

The Android client is an educational interface. It must not present itself as a diagnostic or prescribing application.

Sensitive Atlas content must be retrieved only through an authenticated, encrypted backend once that backend exists. Never embed API keys or private signing material in the APK.

## Build targets

Use Android Studio and Gradle. For current Play submissions, verify Google's current target-API requirement before each release.
