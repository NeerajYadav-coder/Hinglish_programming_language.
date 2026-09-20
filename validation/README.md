# Hinglish Real-World Validation Corpus (v1.0.0)

This directory contains empirical validation programs developed during **Step 12: Real-World Validation & v1.1 Discovery**.

Unlike synthetic unit tests, these programs represent realistic use cases across foundational domains, assessing language ergonomics, standard library interoperability, error mapping, and developer tooling (LSP, DAP, Formatter, Linter).

## Structure

```text
validation/
├── 01_basics/
│   ├── calculator.hin        # Math operations, history, math stdlib, ZeroDivisionError handling
│   └── text_stats.hin        # String tokenization, frequency analysis, word statistics
├── 02_data_processing/
│   ├── json_analytics.hin    # json stdlib deserialization, list comprehension filtering & metrics
│   └── csv_pipeline.hin      # In-memory StringIO, csv.DictReader & DictWriter, payroll calculation
├── 03_oop/
│   └── inventory_system.hin  # Domain hierarchy, inheritance, polymorphism, custom errors, @property
├── 04_cli/
│   └── task_tracker.hin      # CLI subcommand routing with structural pattern matching (milaao / vichaar)
├── 05_file_processing/
│   └── log_analyzer.hin      # File context managers (saath/khol), regex pattern matching, error classification
├── 06_async/
│   └── async_job_queue.hin   # Asynchronous tasks (asamanantar kaam, intezaar, asyncio.gather)
├── 07_multifile/
│   ├── math_helpers.hin      # Math algorithms (factorial, prime check, fibonacci, mean)
│   ├── string_helpers.hin    # String utilities (slugify, truncate, word_count, title_case)
│   └── runner.hin            # Multi-file module importing and integration runner
└── 08_real_project/
    ├── config.hin            # Application settings, tax & discount rates, banners
    ├── utils.hin             # Regex validation, token hashing (sha256), currency formatting
    ├── models.hin            # Customer, OrderItem, Order entities, OrderValidationError
    ├── services.hin          # BillingService with tier loyalty logic, NotificationService
    └── main.hin              # End-to-end execution pipeline & order routing
```

## Running the Validation Suite

To run all runnable validation entry points:

```bash
python3 -m hinglish.cli run validation/01_basics/calculator.hin
python3 -m hinglish.cli run validation/01_basics/text_stats.hin
python3 -m hinglish.cli run validation/02_data_processing/json_analytics.hin
python3 -m hinglish.cli run validation/02_data_processing/csv_pipeline.hin
python3 -m hinglish.cli run validation/03_oop/inventory_system.hin
python3 -m hinglish.cli run validation/04_cli/task_tracker.hin
python3 -m hinglish.cli run validation/05_file_processing/log_analyzer.hin
python3 -m hinglish.cli run validation/06_async/async_job_queue.hin
python3 -m hinglish.cli run validation/07_multifile/runner.hin
python3 -m hinglish.cli run validation/08_real_project/main.hin
```

## Validating Formatting & Linting

All files in this corpus must pass canonical style checks and zero linter warnings:

```bash
# Check formatting
python3 -m hinglish.cli format --check validation/**/*.hin

# Check linting
python3 -m hinglish.cli lint validation/**/*.hin
```
