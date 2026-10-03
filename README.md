# Ethos Bitcoin — Public Distribution

Ethos Bitcoin is a free public distribution. No Bitcoin payment is required to download it.

## Release artifact

The approved public artifact is [`Copy of Ethos_Bitcoin.xlsx`](./Copy%20of%20Ethos_Bitcoin.xlsx). The repository does not contain a separate private Master. The published spreadsheet is the reviewed Distribution Copy for this release.

Its SHA-256 checksum is recorded in [`distribution_manifest.json`](./distribution_manifest.json). Do not replace the artifact without updating the manifest through review.

## Optional Bitcoin support

Optional support may be sent to the verified public Bitcoin address in `DONATIONS.md` and `distribution_manifest.json`:

`bc1q2tkjmreuv8t9mqsew8l2h0kdvxarym3y6v2ld6`

Support is voluntary. It is not required to download the artifact and does not grant ownership, equity, governance rights, profit participation, investment rights, a security, or a guaranteed return. Bitcoin transfers are generally irreversible; verify the address independently before sending.

## Integrity and release controls

- CI requires exactly one approved artifact with the exact filename `Copy of Ethos_Bitcoin.xlsx`.
- CI verifies the committed SHA-256 and byte size from `distribution_manifest.json`.
- CI validates the Bitcoin address using Bech32 checksum rules.
- CI rejects obvious private-key, seed-phrase, and credential markers in text extracted from the spreadsheet archive.
- The repository uses read-only GitHub Actions permissions and pinned action revisions.

The checksum proves that the downloaded file matches this reviewed release record. It does not prove ownership of the Bitcoin address or provide legal, tax, financial, or compliance advice.

## Other projects

Pathos, Logos, and Steezy are separate projects with separate terms. This repository does not establish their pricing, ownership, licensing, or distribution terms.

## License and terms

Repository scripts and documentation are covered by the repository license. The spreadsheet’s public sharing terms are described in [`DISTRIBUTION_TERMS.md`](./DISTRIBUTION_TERMS.md).