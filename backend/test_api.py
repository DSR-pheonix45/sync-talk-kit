#!/usr/bin/env python3
"""
Test script to verify backend API endpoints and authentication
"""

import asyncio
import httpx
import json
from typing import Optional

BASE_URL = "http://localhost:8000/api"

async def test_health_endpoints():
    """Test health endpoints"""
    print("Testing health endpoints...")

    async with httpx.AsyncClient() as client:
        try:
            # Test healthz
            response = await client.get(f"{BASE_URL}/healthz")
            print(f"✅ Healthz: {response.status_code} - {response.json()}")

            # Test readyz
            response = await client.get(f"{BASE_URL}/readyz")
            print(f"✅ Readyz: {response.status_code} - {response.json()}")

        except Exception as e:
            print(f"❌ Health check failed: {e}")

async def test_workbench_endpoints_without_auth():
    """Test workbench endpoints without authentication (should fail)"""
    print("\nTesting workbench endpoints without auth (should fail)...")

    async with httpx.AsyncClient() as client:
        try:
            # Try to list workbenches without auth
            response = await client.get(f"{BASE_URL}/workbenches")
            print(f"❌ Expected 401, got {response.status_code}")

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                print(f"✅ Correctly got 401: {e.response.json()}")
            else:
                print(f"❌ Unexpected status: {e.response.status_code}")

async def main():
    """Run all tests"""
    print("🚀 Testing Backend API Connection")
    print("=" * 50)

    await test_health_endpoints()
    await test_workbench_endpoints_without_auth()

    print("\n" + "=" * 50)
    print("✅ Basic connectivity tests completed!")
    print("💡 Next: Test with actual Supabase authentication")

if __name__ == "__main__":
    asyncio.run(main())
