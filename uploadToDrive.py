def uploadToDrive(file_vec):
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
    import os
    import sys
    g_login = GoogleAuth()
    g_login.LocalWebserverAuth()
    drive = GoogleDrive(g_login)

    for mp3_file in file_vec.split(","):
        print(file_vec.split(","))
        try:
            with open(mp3_file, 'rb') as outfile: 
                print("Uploading {} to Google Drive...".format(os.path.basename(outfile.name)))
                file_drive = drive.CreateFile({'title': outfile.name, 'mimeType': 'audio/mp3'})
                file_drive.SetContentFile(os.path.abspath(outfile.name))
                file_drive.Upload()
            print("Uploaded {}".format(os.path.basename(outfile.name)))
        except:
            print('Upload attempt unsuccessful. Error msg: ', sys.exc_info()[0])
    
    print("Task complete")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filenames", help="Comma-delimited list of files to upload to Drive.")
    args = parser.parse_args()
    uploadToDrive(file_vec=args.filenames)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass 
