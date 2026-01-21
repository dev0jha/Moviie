print("MAIN FILE STARTED")

from recommender.content_based import recommend

def main():
    movie = input("Enter movie name: ").strip()
    results = recommend(movie)

    if not results:
        print(" Movie not found. Check spelling.")
    else:
        print(f"\n🎬 Recommended movies for '{movie}':")
        for i, m in enumerate(results, 1):
            print(f"{i}. {m}")

if __name__ == "__main__":
    main()