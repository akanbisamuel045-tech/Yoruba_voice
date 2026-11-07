import os,json,wave,random,csv
AUDIO_DIR="dataset/audio"
CSV_PHONE="dataset/labels_phone.csv"
TRAIN_MANIFEST="dataset/train.jsonl"
VAL_MANIFEST="dataset/val.jsonl"
VAL_SPLIT=0.15
RANDOM_SEED=42
def get_dur(p):
    with wave.open(p,"r") as w:
        return round(w.getnframes()/w.getframerate(),3)
phone_labels={}
with open(CSV_PHONE,encoding="utf-8") as f2:
    for row in csv.DictReader(f2):
        phone_labels[row["filename"].strip()]=row["text"].strip().lower()
def slug_to_text(fname):
    name=os.path.splitext(fname)[0]
    parts=name.split("_")
    if parts and parts[-1].isdigit(): parts=parts[:-1]
    return " ".join(parts).lower()
wav_files=sorted([f for f in os.listdir(AUDIO_DIR) if f.endswith(".wav")])
entries=[]
skipped=0
for fname in wav_files:
    path=os.path.join(AUDIO_DIR,fname)
    abs_path=os.path.abspath(path).replace(chr(92),chr(47))
    text=phone_labels.get(fname,slug_to_text(fname))
    if not text: skipped+=1; continue
    try:
        dur=get_dur(path)
    except: skipped+=1; continue
    if dur<0.3: skipped+=1; continue
    entries.append({"audio_filepath":abs_path,"duration":dur,"text":text})
random.seed(RANDOM_SEED)
random.shuffle(entries)
split=int(len(entries)*(1-VAL_SPLIT))
train_data=entries[:split]
val_data=entries[split:]
for fpath,data,label in [(TRAIN_MANIFEST,train_data,"train"),(VAL_MANIFEST,val_data,"val")]:
    with open(fpath,"w",encoding="utf-8") as f3:
        for entry in data:
            f3.write(json.dumps(entry,ensure_ascii=False)+"\n")
    print(label+": "+str(len(data))+" entries")
print("Skipped: "+str(skipped))
print("Total: "+str(len(entries)))
