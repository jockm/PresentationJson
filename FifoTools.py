import os
import posix


class FifoTools:
    @staticmethod
    def getFifoPath(fname: str) -> str:
        PIPELINES_ROOT: str = "/tmp/pjpipelines"
        ret = os.path.join(PIPELINES_ROOT, fname)
        return ret

    @staticmethod
    def createFifo(name) -> bool:
        if not os.path.exists(FifoTools.getFifoPath("")):
            os.makedirs(FifoTools.getFifoPath(""))

        try:
            print("Creating input pipe")
            posix.mkfifo(FifoTools.getFifoPath(name))
            print("Named pipe created successfully!")
        except FileExistsError:
            print("Named pipe already exists! But that is ok!")
        except OSError as e:
            print(f"Named pipe creation failed: {e}")
            return False

        return True

    @staticmethod
    def removeFifo(name) -> bool:
        try:
            posix.remove(FifoTools.getFifoPath(name))
        except OSError as e:
            print(f"Named pipe destruction failed: {e}")
            return False

        return True
