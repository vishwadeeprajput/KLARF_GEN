# Architecture

The application is structured around a modular clean architecture:
- `main.py`: Entry point and CLI user interaction.
- `generator.py`: Core engine that coordinates parsing, generating, and writing.
- `parser.py`: Reads the KLARF file, extracts die map, and separates header/footer logic.
- `writer.py`: Reconstructs the KLARF 1.2 spec with new generated defect lines and updated SummaryList.
- `distributions.py`: Houses mathematical modeling for semiconductor defects.
