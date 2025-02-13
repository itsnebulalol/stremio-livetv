# stremio-livetv

Proxy service that converts Stremio Live TV addons into a M3U8 playlist.

## Setup

```yaml
services:
  stremio-livetv:
    image: itsnebulalol/stremio-livetv:latest
    container_name: stremio-livetv
    ports:
      - "5000:5000"
    volumes:
      - ./config.json:/app/config.json
    restart: unless-stopped
```

Or using Docker CLI:
```bash
docker run -d \
    -p 5000:5000 \
    -v $(pwd)/config.json:/app/config.json \
    --name stremio-livetv \
    itsnebulalol/stremio-livetv:latest
```

## Using with Jellyfin

Add `http://ip:5000/playlist.m3u8` to Jellyfin.
