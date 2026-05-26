# Diamond example pseudopotentials

This directory bundles the two small Carbon pseudopotentials needed by the Diamond C K-edge practice example so beginners do not need to find the Quantum ESPRESSO source tree just to run the first example.

Files:

- `C_PBE_TM_2pj.UPF` — normal Carbon pseudopotential.
- `Ch_PBE_TM_2pj.UPF` — Carbon core-hole pseudopotential used by the QE XSpectra Diamond example.

Source:

- Quantum ESPRESSO repository: <https://github.com/QEF/q-e>
- Original path: `XSpectra/examples/pseudo/`
- Local source used when adding these files: `QEF/q-e` `develop` at commit `8b164e93c`

Checksums:

```text
9d85a4306edf1673cc4af0dae25046a5693292f3dd1ffdcf9bb0b24349d52a8a  C_PBE_TM_2pj.UPF
6d463516627c1e631afbd40bf367e53c89e13542ede46d9986a3e5e39561c7c6  Ch_PBE_TM_2pj.UPF
```

These files come from the Quantum ESPRESSO distribution. The QE README states that material in that distribution is free software under the GNU General Public License, version 2 or later. Keep this provenance note with redistributed copies, and cite Quantum ESPRESSO / XSpectra appropriately when using tutorial results.
