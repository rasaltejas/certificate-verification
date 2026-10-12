# Certificate Verification

A Streamlit demo for issuing and verifying academic certificates against a
proof-of-work blockchain.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Deploy this repository with Streamlit Community Cloud, select `app.py` as the
entry point, and let the platform install dependencies from `requirements.txt`.
For another hosting platform, use `streamlit run app.py` as the start command
and expose the port configured by that platform.

## Storage note

The blockchain currently lives in application memory. It is shared by users of
the same running process and is cleared whenever the app restarts or is
redeployed. Use persistent storage and appropriate access controls before
using this demo for real certificate records.
