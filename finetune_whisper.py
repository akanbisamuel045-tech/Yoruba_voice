# -*- coding: utf-8 -*-
import os, json, torch
import whisper
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
from whisper.tokenizer import get_tokenizer

TRAIN_MANIFEST = "dataset/train.jsonl"
VAL_MANIFEST   = "dataset/val.jsonl"
OUTPUT_DIR     = "models/whisper_yoruba"
WHISPER_MODEL  = "small"
EPOCHS         = 10
BATCH_SIZE     = 2
LEARNING_RATE  = 1e-5
MAX_DURATION   = 10
LANGUAGE       = "yo"
DEVICE         = "cuda" if torch.cuda.is_available() else "cpu"

os.makedirs(OUTPUT_DIR, exist_ok=True)
print("Device: " + DEVICE)


class YorubaDataset(Dataset):
    def __init__(self, manifest_path, tokenizer, n_mels):
        self.samples   = []
        self.tokenizer = tokenizer
        self.n_mels    = n_mels
        with open(manifest_path, encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line.strip())
                if entry["duration"] <= MAX_DURATION:
                    self.samples.append(entry)
        print("Loaded " + str(len(self.samples)) + " samples from " + manifest_path)

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        sample  = self.samples[idx]
        audio   = whisper.load_audio(sample["audio_filepath"])
        audio   = whisper.pad_or_trim(audio)
        mel     = whisper.log_mel_spectrogram(audio, n_mels=self.n_mels).to(DEVICE)
        text    = sample["text"]
        tokens  = [self.tokenizer.sot]
        tokens += self.tokenizer.encode(text)
        tokens += [self.tokenizer.eot]
        return {"mel": mel, "tokens": torch.tensor(tokens, dtype=torch.long)}


def collate_fn(batch):
    mels    = torch.stack([b["mel"] for b in batch])
    max_len = max(b["tokens"].shape[0] for b in batch)
    tokens  = torch.zeros(len(batch), max_len, dtype=torch.long)
    for i, b in enumerate(batch):
        tokens[i, :b["tokens"].shape[0]] = b["tokens"]
    return {"mel": mels, "tokens": tokens}


def train():
    print("Loading Whisper " + WHISPER_MODEL + "...")
    model     = whisper.load_model(WHISPER_MODEL).to(DEVICE)
    tokenizer = get_tokenizer(multilingual=True, language=LANGUAGE, task="transcribe")
    n_mels    = model.dims.n_mels

    train_ds = YorubaDataset(TRAIN_MANIFEST, tokenizer, n_mels)
    val_ds   = YorubaDataset(VAL_MANIFEST,   tokenizer, n_mels)
    train_dl = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,  collate_fn=collate_fn)
    val_dl   = DataLoader(val_ds,   batch_size=BATCH_SIZE, shuffle=False, collate_fn=collate_fn)

    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)
    scheduler = CosineAnnealingLR(optimizer, T_max=EPOCHS)
    best_val  = float("inf")

    for epoch in range(1, EPOCHS + 1):
        model.train()
        train_loss = 0
        for batch in train_dl:
            mel          = batch["mel"].to(DEVICE)
            tokens       = batch["tokens"].to(DEVICE)
            labels       = tokens[:, 1:].contiguous()
            input_tokens = tokens[:, :-1].contiguous()
            logits       = model(mel, input_tokens)
            loss         = torch.nn.functional.cross_entropy(
                logits.view(-1, logits.size(-1)),
                labels.view(-1),
                ignore_index=0
            )
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            train_loss += loss.item()

        scheduler.step()
        avg_train = train_loss / len(train_dl)

        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch in val_dl:
                mel          = batch["mel"].to(DEVICE)
                tokens       = batch["tokens"].to(DEVICE)
                labels       = tokens[:, 1:].contiguous()
                input_tokens = tokens[:, :-1].contiguous()
                logits       = model(mel, input_tokens)
                loss         = torch.nn.functional.cross_entropy(
                    logits.view(-1, logits.size(-1)),
                    labels.view(-1),
                    ignore_index=0
                )
                val_loss += loss.item()

        avg_val = val_loss / len(val_dl)
        print("Epoch " + str(epoch) + "/" + str(EPOCHS) +
              "  train=" + str(round(avg_train, 4)) +
              "  val=" + str(round(avg_val, 4)))

        if avg_val < best_val:
            best_val  = avg_val
            save_path = os.path.join(OUTPUT_DIR, "whisper_yoruba_best.pt")
            torch.save(model.state_dict(), save_path)
            print("  Best model saved -> " + save_path)

    final = os.path.join(OUTPUT_DIR, "whisper_yoruba_final.pt")
    torch.save(model.state_dict(), final)
    print("Training complete! Final: " + final)


if __name__ == "__main__":
    train()
