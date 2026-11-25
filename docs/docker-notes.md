# My first docker container

After running `docker run -d --name web -p 8080:80 nginx`, I checked with `docker ps`. A row appeared with NAMES=web, STATUS=Up, and PORTS=0.0.0.0:8080->80/tcp, which matches my run command.

## Container details
- **Default Page Folder**: By default, nginx's default page is found through this path, `/usr/share/nginx/html`.
- **Main Config File**: On the other hand, nginx's config file is this specified path, `/etc/nginx/nginx.conf`.
- **Container's IP Address**: The container's IP address can be found typing this command, `docker inspect web` and checking under `Network Settings`, `Networks` then `IPAddress`. A much easier and direct way is through this command, `$(docker inspect --format '{{.NetworkSettings.IPAddress}}' web)`
- **Port Mapping**: Port mapping, on the other hand, can also be found in the contents of `docker inspect web` under `Network Settings` then `Ports`. Again, a direct command for this is `docker port web`
- **Image ID**: The container's `image id` is easily found at the top, look for `id` (the container's id) then under it, `Image` is where the image id is located. A quick command is `$(docker inspect --format '{{.Image}}' web)`