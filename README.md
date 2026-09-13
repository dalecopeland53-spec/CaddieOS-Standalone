# CaddieOS Standalone

Standalone Expo/React Native caddie app with a separate optional Node/PostGIS backend.

## Android APK

The Expo app lives at the repository root so EAS can build it directly.

```bash
npm install
npx eas build -p android --profile preview
```

The `preview` profile produces an installable Android APK.

## Identity

- App name: CaddieOS
- Expo slug: `caddieos-standalone`
- Android package: `com.dalecopeland.caddieos`
- iOS bundle ID: `com.dalecopeland.caddieos`

## Backend

The optional backend is isolated in `backend/` and can be started with Docker using `docker-compose.yml` and `deploy.sh`.
