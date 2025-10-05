#!/bin/bash

# Test Script for Will It Rain On My Parade?
# This script tests all major endpoints of the application

echo "🧪 Testing Will It Rain On My Parade? API"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

BASE_URL="http://localhost:8000"

# Test 1: Health Check
echo "Test 1: Health Check"
echo "-------------------"
response=$(curl -s ${BASE_URL}/health)
if echo "$response" | grep -q "ok"; then
    echo -e "${GREEN}✓ PASSED${NC}: Health check successful"
    echo "Response: $response"
else
    echo -e "${RED}✗ FAILED${NC}: Health check failed"
    echo "Response: $response"
fi
echo ""

# Test 2: Forecast for past date
echo "Test 2: Forecast for Past Date (Real Data)"
echo "------------------------------------------"
response=$(curl -s -X POST ${BASE_URL}/api/forecast \
    -H "Content-Type: application/json" \
    -d '{
        "event_date": "2025-10-04",
        "query": "New York, NY"
    }')
if echo "$response" | grep -q "precipitation_probability"; then
    echo -e "${GREEN}✓ PASSED${NC}: Past date forecast successful"
    echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
else
    echo -e "${RED}✗ FAILED${NC}: Past date forecast failed"
    echo "Response: $response"
fi
echo ""

# Test 3: Forecast for future date
echo "Test 3: Forecast for Future Date (Historical Proxy)"
echo "---------------------------------------------------"
response=$(curl -s -X POST ${BASE_URL}/api/forecast \
    -H "Content-Type: application/json" \
    -d '{
        "event_date": "2025-12-25",
        "query": "Paris, France"
    }')
if echo "$response" | grep -q "precipitation_probability"; then
    echo -e "${GREEN}✓ PASSED${NC}: Future date forecast successful"
    echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
else
    echo -e "${RED}✗ FAILED${NC}: Future date forecast failed"
    echo "Response: $response"
fi
echo ""

# Test 4: Forecast with coordinates
echo "Test 4: Forecast with Coordinates"
echo "---------------------------------"
response=$(curl -s -X POST ${BASE_URL}/api/forecast \
    -H "Content-Type: application/json" \
    -d '{
        "event_date": "2025-10-04",
        "location": {
            "latitude": 35.6762,
            "longitude": 139.6503,
            "name": "Tokyo"
        }
    }')
if echo "$response" | grep -q "precipitation_probability"; then
    echo -e "${GREEN}✓ PASSED${NC}: Coordinate-based forecast successful"
    echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
else
    echo -e "${RED}✗ FAILED${NC}: Coordinate-based forecast failed"
    echo "Response: $response"
fi
echo ""

# Test 5: Statistics endpoint
echo "Test 5: Statistics Endpoint"
echo "---------------------------"
response=$(curl -s ${BASE_URL}/api/stats)
if echo "$response" | grep -q "total_forecasts"; then
    echo -e "${GREEN}✓ PASSED${NC}: Statistics endpoint successful"
    echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
else
    echo -e "${RED}✗ FAILED${NC}: Statistics endpoint failed"
    echo "Response: $response"
fi
echo ""

# Test 6: Rate limiting
echo "Test 6: Rate Limiting"
echo "--------------------"
echo "Sending 65 requests to test rate limit (60/min)..."
count=0
for i in {1..65}; do
    response=$(curl -s -o /dev/null -w "%{http_code}" ${BASE_URL}/health)
    if [ "$response" = "429" ]; then
        count=$((count + 1))
    fi
done

if [ $count -gt 0 ]; then
    echo -e "${GREEN}✓ PASSED${NC}: Rate limiting is working (got $count 429 responses)"
else
    echo -e "${RED}✗ WARNING${NC}: Rate limiting may not be working as expected"
fi
echo ""

# Test 7: Error handling
echo "Test 7: Error Handling (Invalid Request)"
echo "---------------------------------------"
response=$(curl -s -X POST ${BASE_URL}/api/forecast \
    -H "Content-Type: application/json" \
    -d '{"event_date": "2025-12-25"}')
if echo "$response" | grep -q "detail"; then
    echo -e "${GREEN}✓ PASSED${NC}: Error handling works correctly"
    echo "Response: $response"
else
    echo -e "${RED}✗ FAILED${NC}: Error handling not working"
    echo "Response: $response"
fi
echo ""

# Summary
echo "=========================================="
echo "🎉 Test Suite Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Open http://localhost:5173 in your browser"
echo "2. Try the interactive UI"
echo "3. Check API docs at http://localhost:8000/docs"
echo ""
echo "For deployment, see docs/DEPLOYMENT.md"
echo ""
