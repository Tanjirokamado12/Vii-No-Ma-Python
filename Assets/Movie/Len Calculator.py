import argparse
from time import gmtime, strftime


def get_mobiclip_length(file_data: bytes) -> str:
    # FPS is stored at 0xC - 0xF (4 bytes)
    raw_fps = int.from_bytes(file_data[0xC:0x10], byteorder="little")

    # Chunk count is stored at 0x10 - 0x13 (4 bytes)
    chunk_count = int.from_bytes(file_data[0x10:0x14], byteorder="little")

    # Convert to usable FPS
    fps = raw_fps / 256 if raw_fps else 1

    # Each chunk = 1 frame
    length_seconds = chunk_count / fps

    # Format as HH:MM:SS (caps at 24h wrap if longer)
    return strftime("%H:%M:%S", gmtime(length_seconds))


def main():
    parser = argparse.ArgumentParser(description="Get Mobiclip video duration")
    parser.add_argument("file", help="Path to movie file")
    args = parser.parse_args()

    with open(args.file, "rb") as f:
        data = f.read()

    duration = get_mobiclip_length(data)
    print(f"Duration: {duration}")


if __name__ == "__main__":
    main()