#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import azure.functions as func
import http_fun as func

from io import BytesIO
from pathlib import Path
from torch import no_grad, LongTensor

import commons
from utils import load_checkpoint, get_hparams_from_file
from models import SynthesizerTrn
from text import text_to_sequence, _clean_text
from urllib.parse import unquote

from scipy.io.wavfile import write
import traceback
from web_utils import wav2

class Cleaner():
    def __init__(self, configfile: str):
        self.cleanernames = get_hparams_from_file(str(Path(__file__).parent/configfile)).data.text_cleaners

    def main(self, req: func.HttpRequest) -> func.HttpResponse:
        text = req.params.get('text')
        if not text:
            return func.HttpResponse(
                "400 BAD REQUEST: null text",
                status_code=400
            )
        try:
            return func.HttpResponse(
                _clean_text(unquote(text), self.cleanernames),
                status_code=200
            )
        except Exception as e:
            print(e)
            traceback.print_exc()
            return func.HttpResponse(
                "400 BAD REQUEST: invalid text",
                status_code=400
            )


class Speaker():
    def __init__(self, configfile: str, pthfile: str):
        self.hps_ms = get_hparams_from_file(str(Path(__file__).parent/configfile))
        self.net_g_ms = SynthesizerTrn(
            len(self.hps_ms.symbols),
            self.hps_ms.data.filter_length // 2 + 1,
            self.hps_ms.train.segment_size // self.hps_ms.data.hop_length,
            n_speakers=self.hps_ms.data.n_speakers,
            **self.hps_ms.model)
        _ = self.net_g_ms.eval()
        load_checkpoint(str(Path(__file__).parent/pthfile), self.net_g_ms)
        # print(self.hps_ms.speakers)


    def get_text(self, text: str, cleaned=False):
        if cleaned:
            text_norm = text_to_sequence(text, self.hps_ms.symbols, [])
        else:
            text_norm = text_to_sequence(text, self.hps_ms.symbols, self.hps_ms.data.text_cleaners)
        if self.hps_ms.data.add_blank:
            text_norm = commons.intersperse(text_norm, 0)
        text_norm = LongTensor(text_norm)
        return text_norm
    
    def getSpeakers(self):
        # print(self.hps_ms.speakers)
        return self.hps_ms.speakers

    def main(self, req: func.HttpRequest) -> func.HttpResponse:
        text = req.params.get('text')
        cleantext = req.params.get('cleantext')
        if not text and not cleantext:
            return func.HttpResponse(
                "400 BAD REQUEST: null text",
                status_code=400,
                mimetype=''
            )
        if text and cleantext:
            return func.HttpResponse(
                "400 BAD REQUEST: text and cleantext cannot be set both",
                status_code=400,
                mimetype=''
            )
        cleaned = False
        if cleantext:
            cleaned = True
            text = cleantext
        speaker_id = req.params.get('id')
        if not speaker_id:
            return func.HttpResponse(
                "400 BAD REQUEST: null speaker id",
                status_code=400,
                mimetype=''
            )
        try:
            speaker_id = int(speaker_id)
        except:
            return func.HttpResponse(
                "400 BAD REQUEST: invalid speaker id",
                status_code=400,
                mimetype=''
            )
        if speaker_id not in range(self.hps_ms.data.n_speakers):
            return func.HttpResponse(
                "400 BAD REQUEST: speaker id out of range",
                status_code=400,
                mimetype=''
            )
        format = req.params.get('format')
        if not format: format = "ogg"
        if format not in ("ogg", "mp3", "wav"):
            return func.HttpResponse(
                "400 BAD REQUEST: invalid format",
                status_code=400,
                mimetype=''
            )
        try:
            stn_tst = self.get_text(unquote(text), cleaned)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return func.HttpResponse(
                "400 BAD REQUEST: invalid text",
                status_code=400,
                mimetype=''
            )
        try:
            with no_grad():
                x_tst = stn_tst.unsqueeze(0)
                x_tst_lengths = LongTensor([stn_tst.size(0)])
                sid = LongTensor([speaker_id])
                audio = self.net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()
                with BytesIO() as f:
                    write(f, self.hps_ms.data.sampling_rate, audio)
                    if format == "wav":
                        return func.HttpResponse(
                            f.getvalue(),
                            status_code=200,
                            mimetype="audio/wav",
                            # fileObject = f,
                        )
                    else:
                        f.seek(0, 0)
                        with BytesIO() as ofp:
                            wav2(f, ofp, format)
                            return func.HttpResponse(
                                ofp.getvalue(),
                                status_code=200,
                                mimetype="audio/mpeg" if format == "mp3" else "audio/ogg",
                                # fileObject = ofp,
                            )
        except Exception as e:
            return func.HttpResponse(
                        "500 Internal Server Error\n"+str(e),
                        status_code=500,
                        mimetype=''
                    )
