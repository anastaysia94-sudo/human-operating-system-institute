# HOSI Android APK/AAB Build Plan

Start web-first; add native Android after the IA/API stabilizes.

1. Install Android Studio.
2. Create a Kotlin project.
3. Use a stable application ID such as `org.hosi.institute`.
4. Build Home, Colleges, Course Reader, Research Library, Atlas, Progress, Settings.
5. Keep API keys and signing secrets out of source.
6. Use HTTPS for backend calls.
7. Add scalable text, content descriptions, focus order and touch-target accessibility.
8. Build debug APKs for device testing.
9. Create and protect a release signing key.
10. Build signed release APK/AAB with Gradle.
11. Use GitHub Actions for repeatable test/build automation.

Example commands:
- `./gradlew assembleDebug`
- `./gradlew assembleRelease`
- `./gradlew bundleRelease`

Official references:
- https://developer.android.com/studio
- https://developer.android.com/build
- https://developer.android.com/studio/publish/preparing

An APK alone does not provide an LMS, database, authentication, or Atlas persistence.