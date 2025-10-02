from PIL import Image
from pathlib import Path
import json
from braille_utils import dotpattern_to_unicode, estimate_space_threshold

# import strategies
from braille_transcriptor.strategies.english import EnglishStrategy
from braille_transcriptor.strategies.french import FrenchStrategy
from braille_transcriptor.strategies.arabic import ArabicStrategy
from braille_transcriptor.strategies.russian import RussianStrategy

def _get_strategy(language: str):
    # Language strategy selection
    if language.lower() == "english":
        strategy = EnglishStrategy()
    elif language.lower() == "french": 
        strategy = FrenchStrategy()
    elif language.lower() == "arabic":
        strategy = ArabicStrategy()
    elif language.lower() == "russian":
        strategy = RussianStrategy()
    else:
        strategy = EnglishStrategy()
    
    return strategy

def recognize_characters(crops_dir: Path, model_path: Path, language: str = "English", grade: int = 1, space_factor: float = 1.2):
    """
    crops_dir: folder with subfolders per document (each contains char_*.jpg and metadata.json)
    model_path: recognition model weights
    language: 'English' | 'French' | 'Arabic' | 'Russian'
    grade: 1 or 2
    space_factor: adjust gap threshold multiplier (1.0..2.0)
    """
    # Import PyTorch modules only when needed to avoid Streamlit compatibility issues
    import torch
    import torchvision.transforms as T
    from models.model_definition import BrailleNet
    
    # class names: my model outputs labels that are string representations of active dots
    # keep the same list (length 63)
    class_names = ['1', '12', '123', '1234', '12345', '123456', '12346', '1235', '12356', '1236', '124', '1245', '12456',
                   '1246', '125', '1256', '126', '13', '134', '1345', '13456', '1346', '135', '1356', '136', '14', '145',
                   '1456', '146', '15', '156', '16', '2', '23', '234', '2345', '23456', '2346', '235', '2356', '236', '24',
                   '245', '2456', '246', '25', '256', '26', '3', '34', '345', '3456', '346', '35', '356', '36', '4', '45',
                   '456', '46', '5', '56', '6']

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    recognition_model = BrailleNet(num_classes=len(class_names)).to(device)
    recognition_model.load_state_dict(torch.load(model_path, map_location=device))
    recognition_model.eval()

    transform = T.Compose([
        T.Grayscale(num_output_channels=1),
        T.Resize((40, 25)),
        T.ToTensor(),
        T.Normalize([0.5], [0.5])
    ])

    strategy = _get_strategy(language)

    for doc_folder in sorted(crops_dir.iterdir()):
        if not doc_folder.is_dir(): 
            continue

        # load metadata
        meta_path = doc_folder / "metadata.json"
        metadata = {}
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        items_meta = metadata.get("items", [])

        per_char_predictions = []
        per_char_unicode = []  # unicode braille per char
        failed = []

        # process files in the order saved (char_1..)
        char_files = sorted([p for p in doc_folder.glob("char_*.jpg")], key=lambda x: int(x.stem.split("_")[1]))
        for idx, char_file in enumerate(char_files, start=1):
            try:
                img = Image.open(char_file).convert("L")
                img_tensor = transform(img).unsqueeze(0).to(device)
                with torch.no_grad():
                    output = recognition_model(img_tensor)
                    pred_class = output.argmax(dim=1).item()
                    pred_label = class_names[pred_class]  # e.g. '123'
                per_char_predictions.append(pred_label)
                per_char_unicode.append(dotpattern_to_unicode(pred_label))
            except Exception as e:
                failed.append(f"{char_file.name}: {str(e)}")
                per_char_predictions.append("?")
                per_char_unicode.append("?")

        # save per-char predictions (one per line) for compatibility
        with open(doc_folder / "predictions.txt", "w", encoding="utf-8") as f:
            for p in per_char_predictions:
                f.write(p + "\n")

        # assemble by rows inserting spaces when gaps are large
        # reconstruct items list in the same order as char files (order field)
        order_map = {item["order"]: item for item in items_meta} if items_meta else {}
        # group by row
        rows = {}
        widths_all = []
        for i, uni in enumerate(per_char_unicode, start=1):
            meta = order_map.get(i)
            row = meta["row"] if meta else 0
            rows.setdefault(row, []).append((meta, uni) if meta else (None, uni))
            if meta:
                widths_all.append(meta.get("width", 0))

        threshold = estimate_space_threshold(widths_all, factor=space_factor)

        assembled_braille = ""
        for r_idx in sorted(rows.keys()):
            row_items = rows[r_idx]
            # if meta exists we have bounding boxes to compute gaps; else just join
            if any(m for m, _ in row_items):
                # build list of (x1,x2,uni)
                seq = []
                for m, uni in row_items:
                    if m:
                        seq.append((m["x1"], m["x2"], uni))
                    else:
                        seq.append((0,0,uni))
                # sort by x1 to be robust
                seq.sort(key=lambda x: x[0])
                for j, (x1, x2, uni) in enumerate(seq):
                    if j == 0:
                        assembled_braille += uni
                        prev_x2 = x2
                    else:
                        gap = x1 - prev_x2
                        if gap > threshold:
                            # insert a braille space — prefer grade1/char space if available
                            try:
                                if hasattr(strategy, 'dictionary') and hasattr(strategy.dictionary, 'grade1_map'):
                                    space_symbol = strategy.dictionary.grade1_map['char'][" "]
                                else:
                                    space_symbol = " "
                            except Exception:
                                space_symbol = " "
                            assembled_braille += space_symbol
                        assembled_braille += uni
                        prev_x2 = x2
            else:
                # no metadata: just join
                for _, uni in row_items:
                    assembled_braille += uni
            # row break -> add regular space
            assembled_braille += " "  # separate rows by space
        assembled_braille = assembled_braille.strip()

        # save assembled braille
        with open(doc_folder / "assembled_braille.txt", "w", encoding="utf-8") as f:
            f.write(assembled_braille)

        # now translate braille  readable text using grade
        try:
            if grade == 1:
                translated = strategy.grade1.from_braille(assembled_braille)
            else:
                translated = strategy.grade2.from_braille(assembled_braille)
        except Exception as e:
            translated = f"[translation error] {str(e)}"

        with open(doc_folder / "translated.txt", "w", encoding="utf-8") as f:
            f.write(translated)

    return crops_dir