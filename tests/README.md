# Recommendation Engine Test Suite

This directory contains a comprehensive test suite for the recommendation engine, implementing the testing strategy outlined in [`recommendation-engine-testing-strategy.md`](../recommendation-engine-testing-strategy.md).

## Test Structure

```
tests/
├── __init__.py                     # Test package initialization
├── README.md                       # This file
├── run_tests.py                    # Main test runner script
├── unit/                          # Unit tests
│   ├── __init__.py
│   ├── test_filters.py            # Tests for filtering logic
│   ├── test_scoring.py            # Tests for scoring algorithms
│   └── test_categorization.py     # Tests for categorization logic
├── integration/                   # Integration tests
│   ├── __init__.py
│   └── test_recommendation_engine.py  # End-to-end system tests
├── golden_datasets/               # Acceptance testing with golden datasets
│   ├── __init__.py
│   ├── test_golden_datasets.py    # Golden dataset test runner
│   └── data_analyst_profile.json  # Sample golden dataset
└── performance/                   # Performance tests
    ├── __init__.py
    └── test_performance.py        # Performance and scalability tests
```

## Running Tests

### Quick Start

Run all tests with the comprehensive test runner:

```bash
python tests/run_tests.py
```

### Test Runner Options

```bash
# Run all tests including performance tests
python tests/run_tests.py

# Skip performance tests for faster execution
python tests/run_tests.py --no-performance

# Run only specific test suite
python tests/run_tests.py --suite unit
python tests/run_tests.py --suite integration
python tests/run_tests.py --suite golden
python tests/run_tests.py --suite performance

# Save detailed report to custom file
python tests/run_tests.py --report my_test_report.txt
```

### Running Individual Test Suites

You can also run individual test suites using Python's unittest module:

```bash
# Unit tests
python -m unittest discover tests/unit -v

# Integration tests
python -m unittest discover tests/integration -v

# Golden dataset tests
python -m unittest discover tests/golden_datasets -v

# Performance tests
python -m unittest discover tests/performance -v
```

## Test Categories

### 1. Unit Tests (`tests/unit/`)

Tests individual components in isolation:

- **`test_filters.py`**: Tests the `FilterEngine` class
  - Salary compatibility filtering
  - Skill-based filtering
  - Interest-based filtering
  - Edge cases and boundary conditions

- **`test_scoring.py`**: Tests the `ScoringEngine` class
  - Skill matching algorithms
  - Interest alignment scoring
  - Salary compatibility scoring
  - Experience level matching
  - Score aggregation and weighting

- **`test_categorization.py`**: Tests the `CategorizationEngine` class
  - Safe Zone, Stretch Zone, Adventure Zone categorization
  - Reason generation
  - Confidence calculation
  - Category distribution analysis

### 2. Integration Tests (`tests/integration/`)

Tests the complete system working together:

- **`test_recommendation_engine.py`**: End-to-end system tests
  - Complete recommendation pipeline
  - Component integration validation
  - Different user profile scenarios
  - Mock data integration
  - Performance consistency
  - Error handling

### 3. Golden Dataset Tests (`tests/golden_datasets/`)

Acceptance testing with curated benchmark datasets:

- **`test_golden_datasets.py`**: Golden dataset test runner
  - Validates recommendations against expected outcomes
  - Ensures consistent behavior across releases
  - Regression testing for recommendation quality

- **`data_analyst_profile.json`**: Sample golden dataset
  - Curated user profile with expected recommendations
  - Includes validation criteria and success metrics
  - Serves as template for additional golden datasets

### 4. Performance Tests (`tests/performance/`)

Tests performance characteristics and scalability:

- **`test_performance.py`**: Performance benchmarks
  - Response time measurements
  - Throughput testing
  - Scalability with different data sizes
  - Memory usage validation
  - Concurrent request handling
  - Performance regression detection

## Test Data

### Mock Data
Tests use mock data from [`recommendation-engine/mock_data.py`](../recommendation-engine/mock_data.py):
- `MOCK_SKILLS`: Sample skills database
- `MOCK_CAREERS`: Sample career templates
- `MOCK_USER_PROFILE`: Primary test user profile
- `ALTERNATIVE_USER_PROFILE`: Secondary test user profile

### Golden Datasets
Curated test datasets with expected outcomes:
- JSON format with user profiles and expected recommendations
- Include validation criteria and success metrics
- Version controlled for regression testing

## Test Coverage

The test suite provides comprehensive coverage of:

### Functional Testing
- ✅ All filtering logic paths
- ✅ All scoring algorithm components
- ✅ All categorization rules
- ✅ End-to-end recommendation pipeline
- ✅ Error handling and edge cases

### Non-Functional Testing
- ✅ Performance benchmarks
- ✅ Scalability validation
- ✅ Memory usage monitoring
- ✅ Concurrent request handling

### Acceptance Testing
- ✅ Golden dataset validation
- ✅ Expected outcome verification
- ✅ Regression testing

## Performance Benchmarks

Current performance targets:
- **Response Time**: < 2.0 seconds per recommendation request
- **Throughput**: > 10 recommendations per second
- **Memory Usage**: Stable across multiple requests
- **Scalability**: Linear scaling with data size

## Adding New Tests

### Unit Tests
1. Create test file in appropriate `tests/unit/` directory
2. Follow naming convention: `test_<module_name>.py`
3. Use `unittest.TestCase` base class
4. Include setup/teardown methods
5. Test both happy path and edge cases

### Golden Datasets
1. Create JSON file in `tests/golden_datasets/`
2. Follow the structure in `data_analyst_profile.json`
3. Include comprehensive validation criteria
4. Add test case in `test_golden_datasets.py`

### Performance Tests
1. Add test methods to `test_performance.py`
2. Use timing measurements and assertions
3. Include performance thresholds
4. Test scalability scenarios

## Continuous Integration

The test suite is designed for CI/CD integration:

- **Exit Codes**: Returns 0 for success, 1 for failures
- **Detailed Reports**: Generates comprehensive test reports
- **Performance Monitoring**: Tracks performance regressions
- **Parallel Execution**: Supports concurrent test execution

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure Python path includes project root
2. **Missing Dependencies**: Install required packages (psutil for performance tests)
3. **Performance Test Failures**: Adjust thresholds based on hardware capabilities
4. **Golden Dataset Mismatches**: Update expected outcomes after algorithm changes

### Debug Mode

Run tests with verbose output for debugging:

```bash
python -m unittest discover tests/ -v
```

### Test Reports

Detailed test reports are saved to `test_report.txt` and include:
- Test execution summary
- Failure details and stack traces
- Performance metrics
- Coverage information

## Best Practices

### Writing Tests
- Use descriptive test method names
- Include docstrings explaining test purpose
- Test one concept per test method
- Use appropriate assertions
- Clean up resources in tearDown

### Test Data
- Use realistic test data
- Avoid hardcoded values where possible
- Create reusable test fixtures
- Document test data assumptions

### Performance Testing
- Set realistic performance thresholds
- Test with various data sizes
- Monitor memory usage
- Include scalability tests

## Contributing

When adding new features to the recommendation engine:

1. **Write Tests First**: Follow TDD approach
2. **Update Golden Datasets**: Add new expected outcomes
3. **Performance Impact**: Measure and document performance changes
4. **Documentation**: Update test documentation

## Support

For questions about the test suite:
- Review the testing strategy document
- Check existing test implementations
- Run tests with verbose output for debugging
- Create issues for test failures or improvements