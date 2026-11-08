# Coding protocol

Every entry of CircaKB was read manually and coded against the rules below. Each
rule is dated and names the dataset that prompted it.

The coding sheet itself was kept in Russian; this is the English rendering. The
original, with the same revision log, is in `data/circadian_age_audit.xlsx`, sheets
*Протокол* (protocol) and *Проверить* (questions).

---

## Rules

1. **Corpus.** All entries of CircaKB, all species. A complete enumeration, not a
   sample. (Until 21 Oct the corpus was restricted to *Mus musculus*; it was
   widened after the non-mouse series were counted.)

2. **Unit of analysis.** One deposited series (GSE). Subseries (wild type and
   knockout) and individual tissues within one GSE collapse to a single row.

3. **Repository.** Entries not from GEO stay in the table with their repository
   named, but do not enter the denominator: field structure differs between
   repositories, so "age present in the record" does not mean the same thing.

4. **Applicability.** If the samples are an immortalized cell line (U2OS, MCF-7,
   MCF-10A, 786-O, NIH3T3 and the like), the age of an animal or donor is not an
   attribute that exists. Such series are marked *age not applicable*, excluded
   from the denominator of the age statistics, and retained in the corpus.
   Organoids and primary cells remain applicable, since the donor's age is
   meaningful.

5. **Retrieval order.** GEO record (sample-level `Characteristics` first, then the
   series description) → the depositing publication → its supplementary material.
   Recording stops at the first source that supplies a value.

6. **Source of record.** The GEO record itself, not the CircaKB fields. CircaKB
   contains omissions where the GEO record holds the data (GSE36871).

7. **Depositing publication.** Only the paper named in the GEO `Citation(s)` field,
   that is, the one that deposited the series. Papers that reuse a dataset
   (meta-analyses listing third-party accessions) are not a source of its metadata.

8. **Empty `Citation(s)`.** Not evidence that no publication exists. A literature
   search is required before recording absence. Two series (GSE54650, GSE414) were
   first coded as having no age; the age was found together with the paper. A paper
   may cite the curated DataSet identifier (GDS) rather than the series accession,
   in which case an accession-based search does not retrieve it (GSE414 cites
   GDS404).

9. **One paper, several series.** Age is attributed only to the series for which it
   is stated in the corresponding section of the methods. It is not carried across
   to the other series of the same paper.

10. **Verbatim recording.** The age is recorded as written, without conversion to
    common units and without rounding.

11. **Statements that are not an age.** Duration of acclimatization to a light
    cycle; duration of a dietary intervention; duration of photoperiodic
    pre-conditioning; culture passage interval; a description of breeding stock
    rather than of the sampled animals; an eligibility window for enrolment.

12. **Relation without a quantity.** A claim such as "age-matched" or "cohoused
    littermates" is not an age value: source *none*, form *relational claim only*.

13. **Several ages in one methods section.** Record the age of the experiment that
    produced the deposited samples. Where that cannot be determined, the form is
    *several irreconcilable values*.

14. **Form of reporting.** Exact value per sample / single exact value for the
    series / narrow range / wide range / cohort mean with a dispersion statistic /
    open-ended bound / relational claim only / several irreconcilable values /
    derivable only from a chain of durations / eligibility window / absent.

15. **Range width.** Recorded as a continuous quantity in weeks, one month taken as
    4.3 weeks. The split into narrow and wide is derived from it; any threshold is
    declared rather than fitted.

16. **Anchor.** *Not stated* means the publication does not say, and is not evidence
    that the age refers to collection. Where an age is given before a named interval
    that precedes sampling, the anchor is the start of the experiment, even if the
    phrase "at the beginning" does not appear.

17. **Citation field.** The column records only whether the GEO `Citation(s)` field
    is populated. An empty field does not mean no publication exists (see rule 8).

18. **Reading.** By eye. A language model may point to a place in a text; only what
    was read directly enters the table.

19. **Year.** The "Public on" date of the GEO record.

20. **Ambiguity.** Rows where a decision was not clear-cut are flagged in the notes
    and listed on the questions sheet.

---

## Revision log

Each entry gives the date, the change, and the dataset that forced it.

- **11 Oct** — retrieval order fixed (GEO → article) after a discrepancy on
  GSE54650, where the same series was coded first as having no age and then as
  6 weeks.
- **11 Oct** — rule added: acclimatization duration is not an age. Prompted by
  GSE10644, GSE25585 and GSE414.
- **21 Oct** — corpus recounted: 79 CircaKB rows proved to be 34 unique mouse GEO
  series.
- **21 Oct** — source category *supplementary material* added (GSE181443).
- **21 Oct** — forms *open-ended bound* (GSE206774) and *relational claim only*
  (GSE175635) added.
- **21 Oct** — anchor column added after GSE184303, GSE214530 and GSE54651.
- **21 Oct** — GSE36871 resolved: sampling times are present in the GEO sample
  titles and absent only from CircaKB. Rule added to read the repository rather
  than the database.
- **21 Oct** — rule added on the depositing publication, after a reuse paper gave
  sampling times that disagreed with the deposited samples.
- **21 Oct** — form *several irreconcilable values* added (GSE208768).
- **21 Oct** — numeric range width introduced as the primary measure, replacing a
  binary threshold that had no justification.
- **23 Oct** — five human cell-line series coded as age not applicable.
- **23 Oct** — the citation column was renamed to record only whether the field is
  populated, after GSE13949 proved to have an empty field and an existing paper.
- **24 Oct** — GSE414 moved from *no age* to *article*: Rudic et al. (2005) located,
  age stated. Rules added on searching PubMed when `Citation(s)` is empty and on
  papers citing a GDS rather than a GSE.
- **24 Oct** — GSE70384 and GSE70391 confirmed independently by a 2026 study that
  reused them and reported that age and sex are not specified.
- **26 Oct** — form *derivable from a chain of durations* added (GSE227724). Traps
  added: "adult" describing broodstock (GSE37332), photoperiodic pre-conditioning
  duration (GSE144677).
- **27 Oct** — form *exact value per sample* added (GSE71620, GSE205155): the only
  form in which age can be used as a covariate.
- **27 Oct** — form *cohort mean with a dispersion statistic* added (GSE56931,
  GSE122541, GSE205677).
- **27 Oct** — trap added: culture passage interval is not an age (GSE161566).
- **27 Oct** — cross-series dependency recorded: GSE205677 shares control samples
  with GSE182117.
- **28 Oct** — form *eligibility window* added (GSE220120).
- **28 Oct** — GSE414 anchor changed to start of experiment on the verbatim wording
  of Rudic et al. (2005).
- **28 Oct** — corpus fully coded: 48 GEO series in which age is applicable.
- **4 Nov** — **GSE182117 corrected.** It had been coded as having no age, with a
  note that the paper's reference to a supplementary table of donor characteristics
  was broken. The table exists: the supplementary PDF contains both a *Figure S4*
  and a lowercase *table s4*, and the second holds the ages. The claim of a broken
  reference is withdrawn as an error. Source changed to *supplementary material*.
- **4 Nov** — form renamed to *mean ± SD or SEM*: some studies report the standard
  deviation and some the standard error.
- **6 Nov** — rule 1 brought up to date: the corpus covers all CircaKB species. The
  wording restricting it to mouse had persisted since 7 Oct.

---

## Corrections

Two codings were entered, used, and later withdrawn as errors. Both are listed in
the log above and both are kept there rather than quietly repaired:

1. **GSE36871** was recorded as showing a defect in the GEO record (missing sampling
   times). The times are present in the GEO sample titles; the omission is in
   CircaKB. Withdrawn 21 Oct.
2. **GSE182117** was recorded as having a broken reference to a supplementary table.
   The table exists and holds the ages. Withdrawn 4 Nov.
