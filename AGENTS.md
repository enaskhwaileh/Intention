# Repository instructions

- The normative method is `docs/method_contract.md`; superseded implementations remain available only through Git history.
- Keep tests offline and deterministic. External models and datasets are opt-in.
- Never tune on test topics or labels. Split by topic, not action variant.
- Every measured claim must point to an immutable run. Missing results remain missing.
- Never commit credentials, restricted data, downloaded models, or caches.
- Update `STATUS.md` after each verified milestone.
