import pytest

from pipeline.verifier import _DOI_RE, _verify_enrichment, _word_count


def _make_enrichment(**overrides) -> dict:
    base = {
        'id': 'enrich-001',
        'paper_id': 'paper-001',
        'summary': 'Short valid summary with factual content about VO2max gains.',
        'sports': ['running'],
        'body_regions': ['calves', 'quads'],
        'topics': ['vo2max'],
        'evidence_level': 1,
        'study_type': 'RCT',
        'population': 'trained',
        'enrichment_status': 'auto_committed',
        'confidence_sports': 0.90,
        'confidence_regions': 0.80,
        'confidence_topics': 0.88,
        'confidence_evidence': 0.92,
        'papers': {
            'id': 'paper-001',
            'title': 'VO2max improvements from interval training in cyclists',
            'doi': '10.1234/test.2022.001',
        },
    }
    base.update(overrides)
    return base


class TestWordCount:
    def test_empty_string(self):
        assert _word_count('') == 0

    def test_single_word(self):
        assert _word_count('hello') == 1

    def test_counts_correctly(self):
        assert _word_count('one two three four') == 4


class TestDoiPattern:
    def test_valid_doi(self):
        assert _DOI_RE.match('10.1234/test.2022.001')

    def test_valid_doi_complex(self):
        assert _DOI_RE.match('10.1007/s00421-022-04998-9')

    def test_invalid_missing_prefix(self):
        assert not _DOI_RE.match('1234/test.2022')

    def test_invalid_no_suffix(self):
        assert not _DOI_RE.match('10.1234/')

    def test_invalid_random_string(self):
        assert not _DOI_RE.match('not-a-doi')


class TestVerifyEnrichment:
    def test_auto_committed_passes_through(self):
        status, reason = _verify_enrichment(_make_enrichment())
        assert status == 'auto_committed'
        assert reason == ''

    def test_needs_review_passes_through(self):
        enrichment = _make_enrichment(enrichment_status='needs_review')
        status, reason = _verify_enrichment(enrichment)
        assert status == 'needs_review'
        assert reason == ''

    def test_flagged_no_sport_tag(self):
        enrichment = _make_enrichment(sports=[])
        status, reason = _verify_enrichment(enrichment)
        assert status == 'flagged'
        assert 'sport' in reason

    def test_flagged_no_evidence_level(self):
        enrichment = _make_enrichment(evidence_level=None)
        status, reason = _verify_enrichment(enrichment)
        assert status == 'flagged'
        assert 'evidence' in reason

    def test_flagged_summary_too_long(self):
        long_summary = ' '.join(['word'] * 160)
        enrichment = _make_enrichment(summary=long_summary)
        status, reason = _verify_enrichment(enrichment)
        assert status == 'flagged'
        assert 'summary' in reason

    def test_flagged_invalid_doi(self):
        enrichment = _make_enrichment()
        enrichment['papers'] = {'id': 'p1', 'title': 'T', 'doi': 'not-a-valid-doi'}
        status, reason = _verify_enrichment(enrichment)
        assert status == 'flagged'
        assert 'DOI' in reason

    def test_flagged_all_confidence_below_threshold(self):
        enrichment = _make_enrichment(
            confidence_sports=0.50,
            confidence_topics=0.45,
            confidence_evidence=0.55,
        )
        status, reason = _verify_enrichment(enrichment)
        assert status == 'flagged'
        assert 'confidence' in reason

    def test_valid_doi_does_not_flag(self):
        enrichment = _make_enrichment()
        enrichment['papers'] = {'id': 'p1', 'title': 'T', 'doi': '10.1007/s00421-022-04998-9'}
        status, reason = _verify_enrichment(enrichment)
        assert status == 'auto_committed'

    def test_no_doi_does_not_flag(self):
        enrichment = _make_enrichment()
        enrichment['papers'] = {'id': 'p1', 'title': 'T', 'doi': None}
        status, reason = _verify_enrichment(enrichment)
        assert status == 'auto_committed'

    def test_partial_confidence_below_threshold_not_flagged(self):
        # Only sports confidence low — not all three, so not flagged
        enrichment = _make_enrichment(confidence_sports=0.50)
        status, reason = _verify_enrichment(enrichment)
        assert status == 'auto_committed'

    def test_multiple_reasons_concatenated(self):
        enrichment = _make_enrichment(sports=[], evidence_level=None)
        status, reason = _verify_enrichment(enrichment)
        assert status == 'flagged'
        assert ';' in reason
