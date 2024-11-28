### Linux Installation
```
git clone https://github.com/zerodev-exe/reddit2tok
cd reddit2tok
docker compose up -d
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### Windows Installation
```
git clone https://github.com/zerodev-exe/reddit2tok
cd reddit2tok
docker compose up -d
python -m venv .venv
.\venv\Scripts\activate
pip install -r requirements.txt
python3 main.py
```

#### If you have an Nvidia GPU

```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124 --force-reinstall --no-cache
```