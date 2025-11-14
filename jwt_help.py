#!/usr/bin/env python3
"""
JWT Utilities Quick Reference

This script provides a quick overview of available JWT management tools
for the Super-Codex-AI authentication system.
"""

def print_help():
    print("🔐 Super-Codex-AI JWT Management Utilities")
    print("=" * 50)
    
    print("\n🚀 RECOMMENDED: jwt_manager.py (All-in-One)")
    print("   Issue tokens:    python jwt_manager.py issue --user admin --role Heir")
    print("   Verify tokens:   python jwt_manager.py verify <token>")
    print("   Debug tokens:    python jwt_manager.py verify --decode-only <token>")
    
    print("\n📝 Individual Utilities:")
    print("   Issue only:      python issue_token.py --user admin --role Council")
    print("   Verify only:     python verify_token.py <token>")
    
    print("\n🎯 Available Roles:")
    print("   • Heir       - Highest authority level")
    print("   • Council    - Council member access")
    print("   • Elder      - Elder privileges")
    print("   • Custodian  - Standard user access")
    
    print("\n🔑 Key Options:")
    print("   • primary    - Uses SECRET_KEY (default)")
    print("   • secondary  - Uses SECRET_KEY_SECONDARY")
    
    print("\n⏰ Common Expiration Times:")
    print("   • 15 min:    --exp 15")
    print("   • 1 hour:    --exp 60 (default)")
    print("   • 1 day:     --exp 1440")
    print("   • 1 week:    --exp 10080")
    
    print("\n📖 Examples:")
    print("   # Quick admin token")
    print("   python jwt_manager.py issue --user admin --role Heir --exp 30")
    print()
    print("   # Test with secondary key")
    print("   python jwt_manager.py issue --user test --role Council --key secondary --verify")
    print()
    print("   # Debug expired token")
    print("   python jwt_manager.py verify --decode-only <expired_token>")
    
    print("\n📚 Documentation: JWT_TOKEN_ISSUER.md")

if __name__ == "__main__":
    print_help()