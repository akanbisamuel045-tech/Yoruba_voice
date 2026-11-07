# -*- coding: utf-8 -*-
import os, json
import nemo.collections.asr as nemo_asr
from omegaconf import OmegaConf, open_dict
import lightning.pytorch as pl

TRAIN_MANIFEST = "dataset/train.jsonl"
VAL_MANIFEST   = "dataset/val.jsonl"
OUTPUT_DIR     = "models/yoruba_conformer"
EPOCHS         = 20
BATCH_SIZE     = 8

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Build vocab from manifests
chars = set()
for path in [TRAIN_MANIFEST, VAL_MANIFEST]:
    with open(path, encoding="utf-8") as f:
        for line in f:
            chars.update(json.loads(line)["text"])
vocab = sorted(chars)
print(f"Vocab size: {len(vocab)}")

# Load pretrained model
print("Loading pretrained model...")
model = nemo_asr.models.EncDecCTCModel.from_pretrained("stt_en_quartznet15x5")

# Swap vocabulary to Yoruba
model.change_vocabulary(new_vocabulary=vocab)
print("Vocabulary updated.")

# Update data configs
with open_dict(model.cfg):
    model.cfg.train_ds.manifest_filepath = TRAIN_MANIFEST
    model.cfg.train_ds.batch_size = BATCH_SIZE
    model.cfg.train_ds.num_workers = 0
    model.cfg.train_ds.pin_memory = False
    model.cfg.train_ds.labels = None
    model.cfg.validation_ds.manifest_filepath = VAL_MANIFEST
    model.cfg.validation_ds.batch_size = BATCH_SIZE
    model.cfg.validation_ds.num_workers = 0
    model.cfg.validation_ds.pin_memory = False
    model.cfg.validation_ds.labels = None

model.setup_training_data(model.cfg.train_ds)
model.setup_validation_data(model.cfg.validation_ds)

# Freeze encoder, train decoder only
model.encoder.freeze()
model.decoder.unfreeze()
print("Encoder frozen. Training decoder only.")

# Use lightning.pytorch Trainer (same package NeMo uses)
trainer = pl.Trainer(
    max_epochs=EPOCHS,
    accelerator="cpu",
    devices=1,
    log_every_n_steps=5,
    enable_progress_bar=True,
    enable_checkpointing=True,
    default_root_dir=OUTPUT_DIR,
)

print("Starting training...")
trainer.fit(model)

save_path = os.path.join(OUTPUT_DIR, "yoruba_asr_final.nemo")
model.save_to(save_path)
print(f"Model saved to: {save_path}")
print("Training complete!")