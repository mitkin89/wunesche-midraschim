# August Wünsche – German Midrash translations

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24527651.svg)](https://doi.org/10.5281/zenodo.24527651)

[Version 1.0.0](https://github.com/mitkin89/wunesche-midraschim/releases/tag/1.0.0)

<p align="center">
  <img src="portraits/wuensche.jpg" alt="August Wünsche" height="180">
  <br><sub>August Wünsche</sub>
</p>

**English** · [Deutsch](README.de.md)

German Midrash translations by August Wünsche, including the *Mechiltha* translated and annotated with Jakob Winter. This repository brings together the ten works currently bundled with Safran and the Wünsche editions of Bereshit, Shemot and Vayikra Rabbah from Sefaria.

**13 works · 5,897 nonempty text segments · 5,944 segment slots.** Footnotes and HTML formatting are preserved.

| Work | Edition | Nonempty segments | Source |
| --- | --- | ---: | --- |
| [Bemidbar Rabbah](data/Bamidbar_Rabbah.json) | Der Midrasch Bemidbar Rabba. Zum ersten Male ins Deutsche uebertragen von Dr. August Wünsche. Leizig 1885 [de] | 444 | Safran |
| [Bereschit Rabbah](data/Bereshit_Rabbah.json) | Der Midrasch Bereschit Rabba. Zum ersten Male ins Deutsche übertragen von Dr. August Wünsche. Leipzig 1881 [de] | 1,037 | Sefaria |
| [Debarim Rabbah](data/Devarim_Rabbah.json) | Der Midrasch Debarim Rabba; zum ersten Male ins Dt. übertr. von August Wünsche. Leipzig 1882 | 160 | Safran |
| [Echa Rabbati](data/Eikhah_Rabbah.json) | Der Midrasch Echa Rabbati, deutsch von A. Wünsche, Leipzig 1881 (Transkription eScriptorium) | 186 | Safran |
| [Esther Rabbah](data/Esther_Rabbah.json) | Der Midrasch Esther, deutsch von A. Wünsche, Leipzig 1880 (Transkription eScriptorium) | 136 | Safran |
| [Kohelet Rabbah](data/Kohelet_Rabbah.json) | Der Midrasch Kohelet, deutsch von A. Wünsche, Leipzig 1880 (Transkription eScriptorium) | 270 | Safran |
| [Mechiltha (mit Jakob Winter)](data/Mekhilta_DeRabbi_Yishmael.json) | Mechiltha. Ein tannaitischer Midrasch zu Exodus, übersetzt und erläutert von J. Winter und A. Wünsche, Leipzig 1909 | 2,008 | Safran |
| [Midrasch Samuel](data/Midrash_Shmuel.json) | Midrasch Samuel (Aus Israels Lehrhallen V), deutsch von A. Wünsche, Leipzig 1910 (Transkription eScriptorium) | 207 | Safran |
| [Pesikta de-Rav Kahana](data/Pesikta_DeRav_Kahana.json) | Pesikta des Rab Kahana, deutsch von A. Wünsche, Leipzig 1885 (Transkription eScriptorium) | 303 | Safran |
| [Ruth Rabbah](data/Ruth_Rabbah.json) | Der Midrasch Ruth, deutsch von A. Wünsche, Leipzig 1880 (Transkription eScriptorium) | 88 | Safran |
| [Schemot Rabbah](data/Shemot_Rabbah.json) | Der Midrach Schemot Rabba. Zum ersten Male ins Deutsche übertragen von Dr. August Wünsche. Leipzig 1882 [de] | 464 | Sefaria |
| [Schir Haschirim Rabbah](data/Shir_HaShirim_Rabbah.json) | Der Midrasch Schir Haschirim, deutsch von A. Wünsche, Leipzig 1880 (Transkription eScriptorium) | 264 | Safran |
| [Wajikra Rabbah](data/Vayikra_Rabbah.json) | Der Midrach Wajikra Rabba. Zum ersten Male ins Deutsche übertragen von Dr. August Wünsche. Leipzig 1884 [de] | 330 | Sefaria |

## Scope and limits

The collection includes the ten Rabbah works on the Torah and Five Megillot, Pesikta de-Rav Kahana, Midrash Shmuel and the Mechiltha. It collects the available digital editions, not a complete bibliography of everything Wünsche published.

Several Safran editions follow Sefaria segmentation. Their `versionNotes` explicitly exclude introductions, appendices or differing recensions without a corresponding segment. The Mechiltha excludes its introduction, appendix, addenda and indexes. All 47 empty segment slots are retained and have not been filled from another edition. Existing OCR errors, historical spellings and source metadata are preserved. This is not a claim of complete proofreading against the printed editions.

## Files and use

- `data/<Title>.json`: unchanged source files, including edition metadata and `text`.
- `links/`: 21 TSV files of existing Safran references; no full text of linked works. No additional links were generated for the three Sefaria additions.
- `sources/sefaria/`: original downloads and a manifest with URLs, retrieval date, version metadata and SHA-256 hashes.
- `manifest.json`: per-file provenance, exact Safran commit, hashes and corpus counts.
- `scripts/`: synchronization and validation; historical Mechiltha scripts in `scripts/mechilta/`.
- `docs/mechilta/`: historical transcription and segmentation instructions documenting the method.
- `portraits/wuensche.jpg`: the portrait used in Safran.

`text` contains nested lists or named parts as objects. Preserve list positions and empty segments: they are part of the reference structure. Some original files technically label German text as `language: "English"` or `"en"`; the source schema is retained, while the manifest records the actual text language as `de`. HTML markup and footnotes are part of the text.

```sh
python3 scripts/validate.py
python3 scripts/sync_safran.py /path/to/Safran
```

Requires Python 3.9+. Synchronization updates the ten Safran editions and reuses the three locally archived Sefaria downloads; it does not automatically download newer internet versions. Historical Mechiltha scripts require their original OCR/segmentation inputs and contain earlier environment paths. They are not a standalone complete rebuild pipeline.

## Sources and rights

The three additional editions are published on [Sefaria](https://www.sefaria.org/texts/Midrash/Aggadah/Midrash%20Rabbah). Full JSON files come from the public export documented by [Sefaria-Export](https://github.com/Sefaria/Sefaria-Export). The editions explicitly identify Wünsche; no modern English translation was imported. All three acknowledge support by the Alfred Freiherr von Oppenheim Foundation. Specific print sources and NLI links are retained in `versionSource` and the source manifest.

Bereshit and Vayikra are explicitly marked `Public Domain`. Shemot's export has no license field and its version listing has an empty license value; this absence is preserved transparently. Its historical 1882 print is treated separately from new editorial contributions. The other ten files come from [Safran](https://github.com/mitkin89/Safran), with existing `license` and `versionNotes` fields unchanged.

See [LICENSE.md](LICENSE.md). New documentation and editorial preparation: CC BY 4.0; scripts: MIT. These terms do not replace source rights or public-domain notices.

## Citation

Igor Mendel Itkin (ed.): *August Wünsche – Midraschim*. Version 1.0.0, 2026. https://doi.org/10.5281/zenodo.24527651. Please also cite the printed edition used and Sefaria's digitization where applicable. See [CITATION.cff](CITATION.cff).
