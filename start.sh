sudo docker run \
-p 25565:25565 \
-v "<folder in which your store your Minecraft world>":/usr/src/app/world \
-e EULA=true \
-e WHITELIST=false \
-e VERIFY_ACCOUNTS=true \
-e MATRIX_HOMESERVER='<your matrix homeserver>' \
-e MATRIX_USERNAME='<matrix bridge client username>' \
-e MATRIX_PASSWORD='<matrix bridge client password>' \
-e MC_CHANNEL='<channel in which you communicate>' \
-e SERVER_ADDRESS='<ip address where players can connect to the server>' \
mc-bridge