#!/bin/bash
# AXIOM FLAME API Testing and Verification Script

DOMAIN="codexdominion.app"
LOCAL_PORT="8080"

echo "🧪 AXIOM FLAME API Testing Suite"
echo "================================"

# Function to test with colored output
test_endpoint() {
    local url=$1
    local description=$2
    local method=${3:-GET}
    local data=${4:-}
    
    echo -n "Testing $description... "
    
    if [ "$method" = "POST" ]; then
        if curl -f -s -X POST -H "Content-Type: application/json" -d "$data" "$url" > /dev/null 2>&1; then
            echo "✅ PASS"
            return 0
        else
            echo "❌ FAIL"
            return 1
        fi
    else
        if curl -f -s "$url" > /dev/null 2>&1; then
            echo "✅ PASS"
            return 0
        else
            echo "❌ FAIL"
            return 1
        fi
    fi
}

# Test local API (direct)
echo ""
echo "🔧 Local API Tests (Direct Connection)"
echo "-------------------------------------"

test_endpoint "http://localhost:$LOCAL_PORT/health" "Local health endpoint"
test_endpoint "http://localhost:$LOCAL_PORT/" "Local root endpoint"

if curl -f -s "http://localhost:$LOCAL_PORT/health" > /dev/null 2>&1; then
    echo "📊 Local API Response:"
    curl -s "http://localhost:$LOCAL_PORT/health" | python3 -m json.tool 2>/dev/null || curl -s "http://localhost:$LOCAL_PORT/health"
fi

echo ""
echo "🌐 Domain Tests (via nginx proxy)"
echo "--------------------------------"

# Test HTTP redirect
echo -n "Testing HTTP to HTTPS redirect... "
if curl -s -I "http://$DOMAIN/health" | grep -q "301\|302"; then
    echo "✅ PASS"
else
    echo "❌ FAIL (no redirect configured)"
fi

# Test HTTPS health endpoint
test_endpoint "https://$DOMAIN/health" "HTTPS health endpoint"

# Test HTTPS root endpoint  
test_endpoint "https://$DOMAIN/" "HTTPS root endpoint"

# Test ceremonial endpoints
echo ""
echo "🏛️ Ceremonial API Tests"
echo "----------------------"

# Test reasoning endpoint
REASON_DATA='{"actor":"Custodian","realm":"PL-001","capsule":"Test Capsule","intent":"Test.Ceremony","seal":"Eternal"}'
test_endpoint "https://$DOMAIN/reason" "Ceremonial reasoning" "POST" "$REASON_DATA"

if curl -f -s -X POST -H "Content-Type: application/json" -d "$REASON_DATA" "https://$DOMAIN/reason" > /dev/null 2>&1; then
    echo "📊 Reasoning Response Sample:"
    RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d "$REASON_DATA" "https://$DOMAIN/reason")
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
    
    # Extract dispatch_id for further testing
    DISPATCH_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('dispatch_id', ''))" 2>/dev/null || echo "")
    
    if [ ! -z "$DISPATCH_ID" ]; then
        echo ""
        echo "🔄 Testing replay with dispatch_id: $DISPATCH_ID"
        REPLAY_DATA="{\"dispatch_id\":\"$DISPATCH_ID\"}"
        test_endpoint "https://$DOMAIN/replay" "Replay authorization" "POST" "$REPLAY_DATA"
        
        echo "🔍 Testing audit with dispatch_id: $DISPATCH_ID"
        AUDIT_DATA="{\"dispatch_id\":\"$DISPATCH_ID\"}"
        test_endpoint "https://$DOMAIN/audit" "Audit verification" "POST" "$AUDIT_DATA"
    fi
fi

echo ""
echo "🔒 SSL Certificate Tests"
echo "-----------------------"

# Test SSL certificate
echo -n "Testing SSL certificate validity... "
if openssl s_client -connect "$DOMAIN:443" -servername "$DOMAIN" </dev/null 2>/dev/null | openssl x509 -noout -dates > /dev/null 2>&1; then
    echo "✅ PASS"
    echo "📋 Certificate Details:"
    openssl s_client -connect "$DOMAIN:443" -servername "$DOMAIN" </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates 2>/dev/null || echo "Certificate details unavailable"
else
    echo "❌ FAIL"
fi

# Test security headers
echo ""
echo "🛡️ Security Headers Test"
echo "-----------------------"

HEADERS=$(curl -s -I "https://$DOMAIN/health" 2>/dev/null)

check_header() {
    local header=$1
    local description=$2
    echo -n "Checking $description... "
    if echo "$HEADERS" | grep -qi "$header"; then
        echo "✅ PRESENT"
    else
        echo "⚠️ MISSING"
    fi
}

check_header "Strict-Transport-Security" "HSTS header"
check_header "X-Frame-Options" "X-Frame-Options header"
check_header "X-Content-Type-Options" "X-Content-Type-Options header"
check_header "Content-Security-Policy" "CSP header"

echo ""
echo "⚡ Performance Tests"
echo "------------------"

# Test response time
echo -n "Testing response time... "
RESPONSE_TIME=$(curl -s -w "%{time_total}" -o /dev/null "https://$DOMAIN/health" 2>/dev/null)
if [ ! -z "$RESPONSE_TIME" ]; then
    echo "✅ ${RESPONSE_TIME}s"
else
    echo "❌ TIMEOUT"
fi

# Test gzip compression
echo -n "Testing gzip compression... "
if curl -s -H "Accept-Encoding: gzip" -I "https://$DOMAIN/health" | grep -qi "content-encoding.*gzip"; then
    echo "✅ ENABLED"
else
    echo "⚠️ DISABLED"
fi

echo ""
echo "🎯 Final Verification"
echo "=====================" 

echo "Your primary test command:"
echo "curl https://$DOMAIN/health"
echo ""

if curl -f -s "https://$DOMAIN/health" > /dev/null 2>&1; then
    echo "🎉 SUCCESS! AXIOM FLAME API is fully operational"
    echo ""
    echo "📊 Live API Response:"
    curl -s "https://$DOMAIN/health" | python3 -m json.tool 2>/dev/null || curl -s "https://$DOMAIN/health"
    echo ""
    echo "🔗 API Endpoints:"
    echo "  https://$DOMAIN/health  - Health check"
    echo "  https://$DOMAIN/reason  - Ceremonial reasoning"
    echo "  https://$DOMAIN/replay  - Replay authorization"
    echo "  https://$DOMAIN/audit   - Audit verification"
    echo ""
    echo "📱 CLI Usage:"
    echo "  export AXIOM_API=\"https://$DOMAIN\""
    echo "  axiom health"
    echo "  axiom invoke \"PL-001\" \"Sovereign Crown\""
else
    echo "❌ FAILED! API is not responding correctly"
    echo ""
    echo "🔍 Troubleshooting:"
    echo "1. Check service: sudo systemctl status axiom-flame"
    echo "2. Check nginx: sudo systemctl status nginx"
    echo "3. Check logs: sudo journalctl -u axiom-flame -f"
    echo "4. Check SSL: openssl s_client -connect $DOMAIN:443"
fi