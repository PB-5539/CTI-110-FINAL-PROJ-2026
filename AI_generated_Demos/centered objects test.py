import tkinter as tk

# Create main window
root = tk.Tk()
root.title("Two Widgets Centered")

# Create a frame to hold the widgets
frame = tk.Frame(root)
frame.pack(pady=20)  # Add vertical padding

# Create two example widgets
btn1 = tk.Button(frame, text="Button 1")
btn2 = tk.Button(frame, text="Button 2")

# Pack them side-by-side inside the frame
btn1.pack(side=tk.LEFT, padx=10)  # Horizontal padding between buttons
btn2.pack(side=tk.LEFT, padx=10)

# Center the frame itself in the main window
frame.pack(anchor="center")

root.mainloop()
