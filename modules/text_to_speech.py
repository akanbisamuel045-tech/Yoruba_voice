# -*- coding: utf-8 -*-
# modules/text_to_speech.py
# Uses pre-recorded Yoruba audio for responses, falls back to edge-tts

import os
import random
import threading

AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataset", "audio")

# Map response text -> list of matching audio files
RESPONSE_MAP = {
    # ── GREETINGS ──
    "E kaabo! Mo wa nibi fun ẹ.": [
        "beeni_mo_wa_nibi_fun_e_001.wav",
        "mo_wa_nibi_fun_isin_re_001.wav",
        "mo_wa_nibi_bi_ibeere_re_wa_001.wav",
    ],
    "Beeni, mo n gbọ.": [
        "beeni_mo_gbo_e_gangan_001.wav",
    ],
    "Mo wa daadaa, e se.": [
        "mo_wa_daadaa_e_se_001.wav",
    ],
    "Mo wa ni ilera, e dupe.": [
        "mo_wa_ni_ilera_e_dupe_001.wav",
    ],

    # ── NAME ──
    "Oruko mi ni Oluranlọwọ Yoruba.": [
        "mo_wa_nibi_fun_isin_re_001.wav",
    ],

    # ── APPS / OPEN ──
    "Mo n ṣii Chrome.": [
        "mo_n_ṣii_aṣawakiri_fun_ẹ_001.wav",
        "mo_n_ii_facebook_fun_001.wav",
    ],
    "Mo n ṣii Word.": [
        "mo_n_ṣii_word_fun_ẹ_001.wav",
    ],
    "Mo n ṣii VS Code.": [
        "mo_n_ṣii_terminal_fun_ẹ_001.wav",
    ],
    "Mo n ṣii Explorer.": [
        "mo_n_ṣii_oluṣayẹwo_faili_fun_ẹ_001.wav",
        "mo_n_ṣii_oluṣayẹwo_faili_fun_ẹ-1_001.wav",
    ],
    "Mo n ṣii Calculator.": [
        "mo_n_ṣii_iṣiro_fun_ẹ_001.wav",
        "mo_n_ṣii_iṣiro_fun_ẹ-1_001.wav",
    ],
    "Mo n ṣii Notepad.": [
        "mo_n_ṣii_notepad_fun_ẹ_001.wav",
        "mo_n_ṣii_notepad_fun_ẹ_002.wav",
    ],
    "Mo n ṣii Settings.": [
        "mo_n_ṣii_eto_fun_ẹ_001.wav",
        "mo_n_ṣii_eto_windows_fun_ẹ_001.wav",
    ],
    "Mo n ṣii Task Manager.": [
        "mo_n_ṣii_olupamọ_iṣẹ_fun_ẹ_001.wav",
        "mo_n_ṣii_olupamọ_iṣẹ_fun_001.wav",
    ],
    "Mo n ṣii CMD.": [
        "mo_n_ṣii_terminal_fun_ẹ_001.wav",
    ],
    "Mo n ṣii PowerShell.": [
        "mo_n_ṣii_powershell_fun_ẹ_001.wav",
    ],
    "Mo n ṣii WhatsApp.": [
        "mo_n_ṣii_whatsapp_fun_ẹ_001.wav",
        "mo_n_ii_whatsapp_fun_001.wav",
    ],
    "Mo n ṣii Browser.": [
        "mo_n_ṣii_aṣawakiri_fun_ẹ_001.wav",
    ],
    "Mo n ṣii orin.": [
        "mo_n_ṣii_iṣiro_fun_ẹ_001.wav",
    ],
    "Mo n ṣii Excel.": [
        "mo_n_ṣii_excel_fun_ẹ_001.wav",
    ],
    "Mo n ṣii PowerPoint.": [
        "mo_n_ṣii_powerpoint_fun_ẹ_001.wav",
    ],
    "Mo n ṣii Git Bash.": [
        "mo_n_ṣii_git_bash_fun_ẹ_001.wav",
    ],
    "Mo n ṣii kalẹnda.": [
        "mo_n_ṣii_kalẹnda_fun_ẹ_001.wav",
    ],
    "Mo n ṣii kọmputa fun ẹ.": [
        "mo_n_ṣii_kọmputa_fun_ẹ_001.wav",
        "mo_n_ṣii_kọmputa_fun_ẹ_002.wav",
    ],
    "Mo n ṣii maapu fun ẹ.": [
        "mo_n_ṣii_maapu_fun_ẹ_001.wav",
        "mo_n_ii_maapu_fun_001.wav",
    ],
    "Mo n ṣii pẹpẹ iṣakoso fun ẹ.": [
        "mo_n_ṣii_pẹpẹ_iṣakoso_fun_ẹ_001.wav",
        "mo_n_ii_pp_iakoso_001.wav",
    ],
    "Mo n ṣii olupamọ ẹrọ fun ẹ.": [
        "mo_n_ṣii_olupamọ_ẹrọ_fun_ẹ_001.wav",
        "mo_n_ii_olupam_r_001.wav",
    ],
    "Mo n ṣii ipo aladani fun ẹ.": [
        "mo_n_ṣii_ipo_aladani_fun_ẹ_001.wav",
    ],
    "Mo n ṣii taabu titun fun ẹ.": [
        "mo_n_ṣii_taabu_titun_fun_ẹ_001.wav",
    ],
    "Mo n ṣii google fun ẹ.": [
        "mo_n_ṣii_google_fun_ẹ_001.wav",
    ],
    "Mo n ṣii facebook fun ẹ.": [
        "mo_n_ṣii_facebook_fun_ẹ_001.wav",
        "mo_n_ii_facebook_fun_001.wav",
    ],
    "Mo n ṣii instagram fun ẹ.": [
        "mo_n_ṣii_instagram_fun_ẹ_001.wav",
        "mo_n_ii_instagram_fun_001.wav",
    ],
    "Mo n ṣii twitter fun ẹ.": [
        "mo_n_ṣii_twitter_fun_ẹ_001.wav",
        "mo_n_ii_twitter_fun_001.wav",
    ],
    "Mo n ṣii amazon fun ẹ.": [
        "mo_n_ṣii_amazon_fun_ẹ_001.wav",
    ],
    "Mo n ṣii jumia fun ẹ.": [
        "mo_n_ṣii_jumia_fun_ẹ_001.wav",
    ],
    "Mo n ṣii konga fun ẹ.": [
        "mo_n_ṣii_konga_fun_ẹ_001.wav",
    ],
    "Mo n ṣii vpn fun ẹ.": [
        "mo_n_ṣii_vpn_fun_ẹ_001.wav",
        "mo_n_ii_vpn_fun_001.wav",
    ],
    "Mo n ṣii galẹri fun ẹ.": [
        "mo_n_ṣii_galẹri_fun_ẹ_001.wav" if os.path.exists(os.path.join(AUDIO_DIR, "mo_n_ṣii_galẹri_fun_ẹ_001.wav")) else "mo_n_ii_galri_fun_001.wav",
    ],
    "Mo n ṣii fọto fun ẹ.": [
        "mo_n_ṣii_fọto_fun_ẹ_001.wav",
        "mo_n_ṣii_fọto_fun_ẹ_002.wav",
        "mo_n_ii_fto_r_fun_001.wav",
    ],

    # ── WIFI / BLUETOOTH ──
    "Mo n tan wifi.": [
        "mo_n_tan_wifi_fun_ẹ_001.wav",
    ],
    "Mo n pa wifi.": [
        "mo_n_pa_wifi_fun_ẹ_001.wav",
    ],
    "Mo n tan bluetooth.": [
        "mo_n_tan_bluetooth_fun_ẹ_001.wav",
    ],
    "Mo n pa bluetooth.": [
        "mo_n_pa_bluetooth_fun_ẹ_001.wav",
    ],

    # ── VOLUME / BRIGHTNESS ──
    "Mo n gbe ohun soke.": [
        "mo_n_gbe_ohun_soke_fun_ẹ_001.wav",
    ],
    "Mo n din ohun ku.": [
        "mo_n_din_imọlẹ_ku_fun_ẹ_001.wav",
    ],
    "Mo n pa ohun run.": [
        "mo_n_pa_aṣawakiri_fun_ẹ_001.wav",
    ],
    "Mo n gbe imọlẹ soke.": [
        "mo_n_gbe_imọlẹ_soke_fun_ẹ_001.wav",
    ],
    "Mo n din imọlẹ ku.": [
        "mo_n_din_imọlẹ_ku_fun_ẹ_001.wav",
    ],

    # ── LOCK / RESTART / SHUTDOWN ──
    "Mo n di komputa mọ.": [
        "mo_n_jade_kuro_ninu_eto_fun_ẹ_001.wav",
    ],
    "Komputa yoo tun bẹrẹ.": [
        "mo_n_ṣii_kọmputa_fun_ẹ_001.wav",
    ],
    "Komputa yoo pa.": [
        "mo_n_pa_gbogbo_window_fun_ẹ_001.wav",
    ],

    # ── NAVIGATION ──
    "Mo n lọ siwaju fun ẹ.": [
        "mo_n_lọ_siwaju_fun_ẹ_001.wav",
    ],
    "Mo n lọ sẹhin fun ẹ.": [
        "mo_n_lọ_sẹhin_fun_ẹ_001.wav",
    ],

    # ── FILE OPERATIONS ──
    "Mo n fipamọ faili fun ẹ.": [
        "mo_n_fipamọ_faili_fun_ẹ_001.wav",
    ],
    "Mo n daakọ ọrọ fun ẹ.": [
        "mo_n_daakọ_ọrọ_fun_ẹ_001.wav",
    ],
    "Mo n daakọ ọna abẹlẹ fun ẹ.": [
        "mo_n_daakọ_ọna_abẹlẹ_fun_ẹ_001.wav",
    ],
    "Mo n ge ọrọ fun ẹ.": [
        "mo_n_ge_ọrọ_fun_ẹ_001.wav",
    ],
    "Mo n lẹ ọrọ fun ẹ.": [
        "mo_n_lẹ_ọrọ_fun_ẹ_001.wav",
    ],
    "Mo n pa faili fun ẹ.": [
        "mo_n_pa_faili_fun_ẹ_001.wav",
        "mo_n_pa_faili_fun_ẹ_002.wav",
    ],
    "Mo n pa taabu fun ẹ.": [
        "mo_n_pa_taabu_fun_ẹ_001.wav",
    ],
    "Mo n pa gbogbo window fun ẹ.": [
        "mo_n_pa_gbogbo_window_fun_ẹ_001.wav",
    ],
    "Mo n pa itan aṣawakiri fun ẹ.": [
        "mo_n_pa_itan_aṣawakiri_fun_ẹ_001.wav",
    ],
    "Mo n tun ṣe fun ẹ.": [
        "mo_n_tun_ṣe_fun_ẹ_001.wav",
    ],
    "Mo n ṣe ipadabọ faili fun ẹ.": [
        "mo_n_ṣe_ipadabọ_faili_fun_ẹ_001.wav",
    ],
    "Mo n wa faili ti o parẹ fun ẹ.": [
        "mo_n_wa_faili_ti_o_parẹ_fun_ẹ_001.wav",
    ],
    "Mo n pa notepad fun ẹ.": [
        "mo_n_pa_notepad_fun_ẹ_001.wav",
        "mo_n_pa_notepad_fun_ẹ_002.wav",
    ],
    "Mo n pa aṣawakiri fun ẹ.": [
        "mo_n_pa_aṣawakiri_fun_ẹ_001.wav",
    ],
    "Mo n pa data gbangba fun ẹ.": [
        "mo_n_pa_data_gbangba_fun_ẹ_001.wav",
    ],
    "Mo n ṣeto asopọ ayelujara fun ẹ.": [
        "mo_n_ṣeto_asopọ_ayelujara_fun_ẹ_001.wav",
    ],
    "Mo n ṣayẹwo iyara ayelujara rẹ.": [
        "mo_n_ṣayẹwo_iyara_ayelujara_rẹ_001.wav",
    ],
    "Mo n ṣe iṣiro iyara ayelujara fun ẹ.": [
        "mo_n_ṣe_iṣiro_iyara_ayelujara_fun_ẹ_001.wav",
    ],

    # ── SEARCH / NEWS ──
    "Mo n wa iroyin fun ẹ.": [
        "mo_n_wa_iroyin_fun_ẹ_001.wav",
    ],
    "Mo n wa iroyin Naijiria fun ẹ.": [
        "mo_n_wa_iroyin_naijiria_fun_ẹ_001.wav",
    ],
    "Mo n wa iroyin iṣowo fun ẹ.": [
        "mo_n_wa_iroyin_iṣowo_fun_ẹ_001.wav",
    ],
    "Mo n wa iroyin ẹkọ fun ẹ.": [
        "mo_n_wa_iroyin_ẹkọ_fun_ẹ_001.wav",
    ],
    "Mo n wa iroyin ere idaraya fun ẹ.": [
        "mo_n_wa_iroyin_ere_idaraya_fun_ẹ_001.wav",
    ],
    "Mo n wa iye owo dola fun ẹ.": [
        "mo_n_wa_iye_owo_dola_fun_ẹ_001.wav",
    ],
    "Mo n wa iye owo pound fun ẹ.": [
        "mo_n_wa_iye_owo_pound_fun_ẹ_001.wav",
    ],
    "Mo n wa alaye lori wikipedia fun ẹ.": [
        "mo_n_wa_alaye_lori_wikipedia_fun_ẹ_001.wav",
    ],
    "Mo n wa orukọ aare orilede naijiria fun ẹ.": [
        "mo_n_wa_orukọ_aare_orilede_naijiria_fun_ẹ_001.wav",
    ],
    "Mo n wa ibi jijẹ ounjẹ ti o sunmọ ẹ.": [
        "mo_n_wa_ibi_jijẹ_ounjẹ_ti_o_sunmọ_ẹ_001.wav",
    ],
    "Mo n wa ile iwosan ti o sunmọ ẹ.": [
        "mo_n_wa_ile_iwosan_ti_o_sunmọ_ẹ_001.wav",
    ],
    "Mo n wa ile itaja ti o sunmọ ẹ.": [
        "mo_n_wa_ile_itaja_ti_o_sunmọ_ẹ_001.wav",
    ],
    "Mo n wa ileifiowopamo ti o sunmọ ẹ.": [
        "mo_n_wa_ileifiowopamo_ti_o_sunmọ_ẹ_001.wav",
    ],

    # ── THANKS / EXIT ──
    "Ko to nkan, mo dupe.": [
        "kosi_wahala_mo_dupe_001.wav",
        "kosi_wahala_kankan_e_ku_i_001.wav",
    ],
    "Odabo, ki ojo re to dara.": [
        "odabo_001.wav",
        "odabo_002.wav",
        "odabo_003.wav",
        "odabo_response_001.wav",
    ],

    # ── HELP ──
    "Mo le ran ẹ lọwọ pẹlu ọpọlọpọ nkan.": [
        "mo_le_ran__lw_plu_plp_nkan_001.wav",
        "mo_le_ran__lw_plu_akoko_iroyin_orin_ati_p_001.wav",
    ],
    "Mo wa nibi lati ran ẹ lọwọ.": [
        "mo_wa_nibi_lati_ran_e_lowo_001.wav",
        "mo_wa_nibi_lati_ran__lw_001.wav",
    ],

    # ── NOT UNDERSTOOD ──
    "Emi ko ye aṣẹ naa, jọwọ tun sọ.": [
        "mo_wa_nibi_bi_ibeere_re_wa_001.wav",
    ],
    "Emi ko gbọ ohunkohun.": [
        "mo_wa_nibi_fun_002.wav",
    ],

    # ── SYSTEM KEYS ──
    "Mo n tẹ bọtini enter fun ẹ.": [
        "mo_n_tẹ_bọtini_enter_fun_ẹ_001.wav",
        "mo_n_t_btini_enter_fun_001.wav",
    ],
    "Mo n tẹ bọtini escape fun ẹ.": [
        "mo_n_tẹ_bọtini_escape_fun_ẹ_001.wav",
        "mo_n_t_btini_escape_fun_001.wav",
    ],
    "Mo n tẹ bọtini aaye fun ẹ.": [
        "mo_n_tẹ_bọtini_aaye_fun_ẹ_001.wav",
    ],

    # ── PHOTO EDITING ──
    "Mo n ṣatunkọ fọto fun ẹ.": [
        "mo_n_ṣatunkọ_fọto_fun_ẹ_001.wav",
    ],

    # ── DATA ──
    "Mo n ṣeto data gbangba fun ẹ.": [
        "mo_n_ṣeto_data_gbangba_fun_ẹ_001.wav",
    ],
    "Mo n fipamọ oju opo fun ẹ.": [
        "mo_n_fipamọ_oju_opo_fun_ẹ_001.wav",
    ],
    "Mo n jade kuro ninu eto fun ẹ.": [
        "mo_n_jade_kuro_ninu_eto_fun_ẹ_001.wav",
    ],
    "Mo n pa igbasilẹ ohun fun ẹ.": [
        "mo_n_pa_igbasil_ohun_fun_001.wav",
    ],
    "Mo n pa vpn fun ẹ.": [
        "mo_n_pa_vpn_fun_001.wav",
    ],
    "Mo n tun fipamọ faili fun ẹ.": [
        "mo_n_tun_fipam_faili_fun_001.wav",
    ],
}


def _get_audio_path(filename):
    """Return full path if file exists, else None."""
    path = os.path.join(AUDIO_DIR, filename)
    return path if os.path.exists(path) else None


def _play_wav(path):
    """Play a WAV file using pygame."""
    try:
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
    except Exception as e:
        print("Playback error: " + str(e))


def _fallback_tts(text):
    """Fall back to edge-tts Nigerian English voice."""
    try:
        import asyncio, edge_tts, tempfile
        import pygame

        async def _gen():
            tts = edge_tts.Communicate(text, voice="en-NG-AbeoNeural")
            tmp = tempfile.mktemp(suffix=".mp3")
            await tts.save(tmp)
            return tmp

        tmp = asyncio.run(_gen())
        pygame.mixer.init()
        pygame.mixer.music.load(tmp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.remove(tmp)
    except Exception as e:
        print("Fallback TTS error: " + str(e))


def speak(text: str):
    """Play pre-recorded response if available, else fall back to TTS."""
    def _run():
        candidates = RESPONSE_MAP.get(text, [])
        # Pick a random valid file from candidates
        valid = [_get_audio_path(f) for f in candidates if _get_audio_path(f)]
        if valid:
            path = random.choice(valid)
            print("Playing response: " + os.path.basename(path))
            _play_wav(path)
        else:
            print("No recording for: " + text + " — using TTS fallback")
            _fallback_tts(text)

    threading.Thread(target=_run, daemon=True).start()
