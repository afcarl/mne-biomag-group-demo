"""
=================================
Decoding (ML) across time (M/EEG)
=================================

A sliding estimator fits a logistic regression model for every time point.
In this example, we contrast the condition `'famous'` vs `'scrambled'`
and `'famous'` vs `'unfamiliar'` using this approach. The end result is an
averaging effect across sensors. The contrast across different sensors are
combined into a single plot.

Analysis script: :ref:`sphx_glr_auto_scripts_10-sliding_estimator.py`
"""

###############################################################################
# Let us first import the necessary libraries

import os
import os.path as op
import sys

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.stats import sem

sys.path.append(op.join('..', '..', 'processing'))
from library.config import meg_dir  # noqa: E402

###############################################################################
# Now we loop over subjects to load the scores
a_vs_bs = ['face_vs_scrambled', 'famous_vs_unfamiliar']
scores = {'face_vs_scrambled': list(), 'famous_vs_unfamiliar': list()}
for subject_id in range(1, 20):
    subject = "sub%03d" % subject_id
    data_path = os.path.join(meg_dir, subject)

    # Load the scores for the subject
    for a_vs_b in a_vs_bs:
        fname_td = os.path.join(data_path, '%s-td-auc-%s.mat'
                                % (subject, a_vs_b))
        mat = loadmat(fname_td)
        scores[a_vs_b].append(mat['scores'][0])

###############################################################################
# ... and average them
times = mat['times'][0]
mean_scores, sem_scores = dict(), dict()
for a_vs_b in a_vs_bs:
    mean_scores[a_vs_b] = np.mean(scores[a_vs_b], axis=0)
    sem_scores[a_vs_b] = sem(scores[a_vs_b])

###############################################################################
# Let's plot the mean AUC score across subjects
from library.config import set_matplotlib_defaults  # noqa
set_matplotlib_defaults(plt)
colors = ['b', 'g']
fig, ax = plt.subplots(1, figsize=(12, 8))
for c, a_vs_b in zip(colors, a_vs_bs):
    ax.plot(times, mean_scores[a_vs_b], c, label=a_vs_b.replace('_', ' '))
    ax.set(xlabel='Time (s)', ylabel='Area under curve (AUC)')
    ax.fill_between(times, mean_scores[a_vs_b] - sem_scores[a_vs_b],
                    mean_scores[a_vs_b] + sem_scores[a_vs_b],
                    color=c, alpha=0.2)
ax.axhline(0.5, color='k', linestyle='--', label='Chance level')
ax.axvline(0.0, color='k', linestyle='--')
ax.legend()
fig.tight_layout()
fig.savefig(op.join('..', 'figures', 'time_decoding.pdf'),
            bbox_to_inches='tight')
plt.show()

###############################################################################
# It seems that `'famous'` vs `'unfamiliar'` gives much noisier time course of
# decoding scores than `'faces'` vs `'scrambled'`. To verify that this is not
# due to bad subjects:
fig, axes = plt.subplots(4, 5, sharex=True, sharey=True, figsize=(12, 8))
axes = axes.ravel()
for idx in range(19):
    axes[idx].axhline(0.5, color='k', linestyle='--', label='Chance level')
    axes[idx].axvline(0.0, color='k', linestyle='--')
    for a_vs_b in a_vs_bs:
        axes[idx].plot(times, scores[a_vs_b][idx], label=a_vs_b)
        axes[idx].set_title('sub%03d' % (idx + 1))

axes[-1].axis('off')
axes[-2].legend(bbox_to_anchor=(2.35, 0.5), loc='center right', fontsize=12)
fig.text(0.5, 0, 'Time (s)', ha='center', fontsize=16)
fig.text(0.01, 0.5, 'Area under curve (AUC)', va='center',
         rotation='vertical', fontsize=16)
plt.subplots_adjust(bottom=0.06, left=0.06, right=0.98, top=0.95)
plt.show()
