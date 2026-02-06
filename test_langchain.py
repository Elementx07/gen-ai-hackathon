#!/usr/bin/env python3
"""Test script to verify LangChain integration."""
import os
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all new modules can be imported."""
    print("Testing imports...")
    try:
        # Temporarily set PROJECT_ID for import
        old_project_id = os.environ.get("PROJECT_ID")
        os.environ["PROJECT_ID"] = "test-project-id"
        
        from src.models import SiteData, ArtisanInfo, Product
        from src.ai_utils import call_gemini_structured, create_chain
        from src.langchain_prompts import (
            data_extraction_prompt,
            component_generation_prompt,
            page_generation_prompt
        )
        
        # Restore original PROJECT_ID
        if old_project_id:
            os.environ["PROJECT_ID"] = old_project_id
        else:
            del os.environ["PROJECT_ID"]
        
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_pydantic_models():
    """Test Pydantic model validation."""
    print("\nTesting Pydantic models...")
    try:
        from src.models import SiteData, ArtisanInfo, Product
        
        # Test valid data
        artisan = ArtisanInfo(
            name="Test Artisan",
            story="A test story",
            contact="test@example.com",
            address="123 Test St",
            phone="+1-555-0123"
        )
        print(f"✅ Created ArtisanInfo: {artisan.name}")
        
        # Test product
        product = Product(
            id="test-1",
            name="Test Product",
            description="A test product",
            price="$10",
            category="Test",
            imageUrl="/images/test.jpg"
        )
        print(f"✅ Created Product: {product.name}")
        
        return True
    except Exception as e:
        print(f"❌ Pydantic validation failed: {e}")
        return False


def test_prompt_templates():
    """Test LangChain prompt templates."""
    print("\nTesting prompt templates...")
    try:
        from src.langchain_prompts import (
            data_extraction_prompt,
            component_generation_prompt
        )
        
        # Test data extraction prompt
        formatted = data_extraction_prompt.format(
            description="I am a test artisan"
        )
        assert "I am a test artisan" in formatted
        print("✅ Data extraction prompt works")
        
        # Test component generation prompt
        formatted = component_generation_prompt.format(
            component_name="TestComponent",
            site_data='{"test": "data"}'
        )
        assert "TestComponent" in formatted
        print("✅ Component generation prompt works")
        
        return True
    except Exception as e:
        print(f"❌ Prompt template test failed: {e}")
        return False


def test_ai_utils_structure():
    """Test AI utilities structure (without calling actual AI)."""
    print("\nTesting AI utilities structure...")
    try:
        # Temporarily set PROJECT_ID for import
        old_project_id = os.environ.get("PROJECT_ID")
        os.environ["PROJECT_ID"] = "test-project-id"
        
        from src.ai_utils import call_gemini, create_chain
        from langchain_core.output_parsers import StrOutputParser
        
        # Test that we can create a chain
        chain = create_chain(
            "Test prompt: {input}",
            "System prompt",
            StrOutputParser()
        )
        
        # Restore original PROJECT_ID
        if old_project_id:
            os.environ["PROJECT_ID"] = old_project_id
        else:
            del os.environ["PROJECT_ID"]
        
        print("✅ Chain creation works")
        
        return True
    except Exception as e:
        print(f"❌ AI utilities test failed: {e}")
        return False


def test_model_validation():
    """Test Pydantic model field validation."""
    print("\nTesting model field validation...")
    try:
        from src.models import SiteData, Product
        from pydantic import ValidationError
        
        # Test that validation catches missing required fields
        try:
            product = Product(
                id="test",
                name="Test"
                # Missing required fields
            )
            print("❌ Validation should have failed for incomplete product")
            return False
        except ValidationError:
            print("✅ Validation correctly rejects incomplete data")
        
        # Test that validation accepts complete data
        product = Product(
            id="test-1",
            name="Complete Product",
            description="Full description",
            price="$50",
            category="Category",
            imageUrl="/images/test.jpg"
        )
        print(f"✅ Validation accepts complete data: {product.name}")
        
        return True
    except Exception as e:
        print(f"❌ Model validation test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("LangChain Integration Test Suite")
    print("=" * 50)
    
    # Check for required environment variables
    if not os.getenv("PROJECT_ID"):
        print("\n⚠️  Warning: PROJECT_ID not set. AI calls will fail.")
        print("   Set it with: export PROJECT_ID=your-project-id")
    
    # Run tests
    tests = [
        test_imports,
        test_pydantic_models,
        test_prompt_templates,
        test_ai_utils_structure,
        test_model_validation,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
