import clr  # Python.NET for loading .NET DLLs
import sys
import os

# Set the path where your DLL is located
DLL_PATH = os.path.abspath("ecr.dll")  # Adjust this if needed

# Add the DLL directory to sys.path so Python can find it
sys.path.append(os.path.dirname(DLL_PATH))

try:
    # Load the DLL
    clr.AddReference("ecr")  # Reference the assembly
    print("✅ .NET DLL loaded successfully!")
except Exception as e:
    print(f"❌ Failed to load DLL: {e}")
    sys.exit(1)

# Now, try to import the namespace and use the class
try:
    from Accent.Ecr import Ecr  # Import class from the namespace

    # Initialize the class (Modify based on actual constructor requirements)
    ecr_instance = Ecr()
    print("✅ Ecr class initialized successfully!")

    # Example method call (Replace 'MethodName' with actual methods)
    if hasattr(ecr_instance, "SomeMethod"):  # Check if method exists
        result = ecr_instance.SomeMethod()  # Call the method
        print(f"🔹 Method result: {result}")
    else:
        print("⚠️ No such method found in Ecr class.")

except ImportError as e:
    print(f"❌ Could not import namespace: {e}")
except Exception as e:
    print(f"❌ Error while using Ecr class: {e}")
