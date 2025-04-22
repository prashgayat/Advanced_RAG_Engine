# test_memory_utils.py

from memory_utils import MemoryManager

def test_memory_manager():
    print("\n🚀 Running MemoryManager Unit Tests...")

    # Initialize memory manager
    memory = MemoryManager()

    # Test 1: Add user message
    memory.add_user_message("Hello, how are you?")
    assert memory.get_history()[-1] == ("user", "Hello, how are you?"), "User message not saved correctly."

    # Test 2: Add assistant message
    memory.add_assistant_message("I'm fine, thank you!")
    assert memory.get_history()[-1] == ("assistant", "I'm fine, thank you!"), "Assistant message not saved correctly."

    # Test 3: Check history length
    assert len(memory.get_history()) == 2, "History length mismatch."

    # Test 4: Clear memory
    memory.clear()
    assert len(memory.get_history()) == 0, "Memory not cleared properly."

    print("✅ All MemoryManager tests passed successfully!\n")

if __name__ == "__main__":
    test_memory_manager()
