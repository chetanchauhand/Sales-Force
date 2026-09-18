import pygame

pygame.init()
pygame.mixer.init()

print("===== MUSIC PLAYER =====")

pygame.mixer.music.load("song.mp3")

pygame.mixer.music.play()

print("Music is playing...")

while True:

    print("\n1. Pause")
    print("2. Resume")
    print("3. Stop")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        pygame.mixer.music.pause()
        print("Music paused.")

    elif choice == "2":
        pygame.mixer.music.unpause()
        print("Music resumed.")

    elif choice == "3":
        pygame.mixer.music.stop()
        print("Music stopped.")

    elif choice == "4":
        pygame.mixer.music.stop()
        break

    else:
        print("Invalid choice.")