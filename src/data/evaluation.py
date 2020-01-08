"""
Tool to metrics calculation through data and label (string and string).
 * Calculation from Optical Character Recognition (OCR) metrics with editdistance.
"""

import editdistance
import numpy as np


def ocr_metrics(ground_truth, data, predict=None):
    """
    Calculate Character Error Rate (CER), Word Error Rate (WER) and Sequence Error Rate (SER).
        - if `ground_truth` and `data` parameters is entered, one metric will be returned (data);
        - if also `predict` parameter is entered, two metrics will be returned (data and predict | before and after);
    """

    if len(ground_truth) == 0 or len(data) == 0:
        return (1, 1, 1)

    def calculate(ground_truth, arr):
        cer, wer, ser = [], [], []

        for (gt, pd) in zip(ground_truth, arr):
            gt, pd = gt.lower(), pd.lower()

            gt_cer, pd_cer = list(gt), list(pd)
            dist = editdistance.eval(pd_cer, gt_cer)
            cer.append(dist / (max(len(pd_cer), len(gt_cer))))

            gt_wer, pd_wer = gt.split(), pd.split()
            dist = editdistance.eval(pd_wer, gt_wer)
            wer.append(dist / (max(len(pd_wer), len(gt_wer))))

            gt_ser, pd_ser = [gt], [pd]
            dist = editdistance.eval(pd_ser, gt_ser)
            ser.append(dist / (max(len(pd_ser), len(gt_ser))))

        return [cer, wer, ser]

    f_arr = calculate(ground_truth, data)
    f_arr = np.mean(f_arr, axis=1)

    if predict is None:
        return f_arr

    s_arr = calculate(ground_truth, predict)
    mean, std = np.mean(s_arr[0]), np.std(s_arr[0])

    norm = [i for i in range(len(s_arr[0])) if (s_arr[0][i] > mean - 2 * std)]
    norm = [i for i in norm if (s_arr[0][i] < mean + 2 * std)]

    s_arr[0] = [s_arr[0][i] for i in norm]
    s_arr[1] = [s_arr[1][i] for i in norm]
    s_arr[2] = [s_arr[2][i] for i in norm]
    s_arr = np.mean(s_arr, axis=1)

    return f_arr, s_arr
