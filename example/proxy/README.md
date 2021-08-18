### Running this example:
install traefik

run:
```sh
traefik --configFile=traefik.toml
```

then in another shell run:
```sh
uvicorn app:app
```

alternatively, delete `root_path="/api"` from `app.py` and run:
```sh
uvicorn app:app --root-path /api
```
