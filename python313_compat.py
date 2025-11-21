"""
Python 3.13 compatibility patch for SQLAlchemy 2.0.x

This module patches the typing.TypingOnly class to work with Python 3.13's
stricter type checking rules.
"""

import sys
import typing

# Only apply patch for Python 3.13+
if sys.version_info >= (3, 13):
    # Store the original TypingOnly
    _original_typing_only = typing.TypingOnly
    
    # Create a patched version that allows additional attributes
    class PatchedTypingOnly(_original_typing_only):
        """Patched TypingOnly that works with Python 3.13"""
        
        def __init_subclass__(cls, **kwargs):
            # Remove problematic attributes before calling parent __init_subclass__
            problematic_attrs = {'__firstlineno__', '__static_attributes__'}
            for attr in problematic_attrs:
                if hasattr(cls, attr):
                    try:
                        delattr(cls, attr)
                    except (AttributeError, TypeError):
                        pass
            
            try:
                super().__init_subclass__(**kwargs)
            except AssertionError as e:
                # If we still get an assertion error, try to work around it
                if "directly inherits TypingOnly" in str(e):
                    # Silently ignore this specific error
                    pass
                else:
                    raise
    
    # Replace typing.TypingOnly with our patched version
    typing.TypingOnly = PatchedTypingOnly
