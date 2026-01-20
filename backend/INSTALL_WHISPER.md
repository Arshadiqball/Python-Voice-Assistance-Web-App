# Installing Whisper for Python 3.14

If you encounter issues installing Whisper with Python 3.14, try these methods:

## Method 1: Install from GitHub (Recommended)

```bash
pip install git+https://github.com/openai/whisper.git
```

## Method 2: Install with setuptools upgrade

```bash
pip install --upgrade setuptools wheel
pip install openai-whisper
```

## Method 3: Manual installation

```bash
git clone https://github.com/openai/whisper.git
cd whisper
pip install -e .
```

## Method 4: Use Python 3.11 or 3.12 (if available)

If the above methods don't work, consider using Python 3.11 or 3.12 which have better compatibility:

```bash
python3.11 -m venv venv
# or
python3.12 -m venv venv
```

## Verify Installation

After installation, verify it works:

```python
import whisper
model = whisper.load_model("base")
print("Whisper installed successfully!")
```

