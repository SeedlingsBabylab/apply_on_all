## apply.py

`$ python apply.py path/to/subject_files path/to/script.py subject month`

Applies `script.py` to all `sparse_code.cha` corresponding to `subject` and `month`.

`subject` can either be two digits `dd` or `--all`, in which case the script will apply to all subject. The same thing applies for `month`, which can be two digits `dd` or `--all`.

The current version of sub_mo_sparse_code.cha is kept as old_chas/sub_mo_sparse_code_year-month-day.cha, so be careful whenever you apply the script twice in the sae day; you may want to use undo beforehand.

## undo.py

`$ python undo.py path/to/subject_files subject month`

Recovers the latest sparse_code in old_chas and restores it as the main sparse_code, while the current sparse_code is saved in old_chas. Basically just exchanges the place of current sparse_code and latest old_chas/sparse_code.
