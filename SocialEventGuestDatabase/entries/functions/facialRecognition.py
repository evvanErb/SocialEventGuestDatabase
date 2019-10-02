#Python 3.x

import face_recognition
import numpy as np
from ..models import Guest

MIN_MATCHES_REQUIRED = 1
MAX_DISTANCE = 0.58

def hogDetectFaceLocations(image, isBGR=False):
    """
    Take a raw image and run the hog face detection on it
    """

    #Convert from BGR to RGB if needed
    if (isBGR):
        image = image[:, :, ::-1]

	#Run the face detection model to find face locations
    faceLocations = face_recognition.face_locations(image)

    return faceLocations

def numberOfMatches(faceEncoding, knownFaceEncodings):
    """
    Compare face encoding to all known face encodings for this person and
    find the close matches and return their count
    """
    #Get the distances from this encoding to
    #those of all reference images for this person
    distances = face_recognition.face_distance(knownFaceEncodings,
        faceEncoding)

    possibleMathcesCount = 0

    #Look at all matches that have a distance below the MAX_DISTANCE
    #if it's below the threshold value then add +1 to this persons match count
    for distance in distances:
        if (distance <= MAX_DISTANCE):
            possibleMathcesCount += 1

    return possibleMathcesCount

def recognizeFace(database, faceEncoding):
    matches = {}

    #Iterate over all people in the database face encodings and get
    #how many photos per known person matched the unknown face
    for person in database:

        personMatchCount = numberOfMatches(faceEncoding, database[person])

        matches[person] = personMatchCount

    #Iterate over all matches and see who has highest count
    bestMatch = None
    bestMatchCount = 0
    for match in matches:
        if ((matches[match] >= MIN_MATCHES_REQUIRED)
                and (matches[match] > bestMatchCount)):
            bestMatch = match
            bestMatchCount = matches[match]

    return bestMatch

def detectAndRecognizeFacesInImage(image,
    database):
    """
    Detects and recognizies faces in image
    """
    #Detect if there are any faces in the frame and get their locations
    faceLocations = hogDetectFaceLocations(image)

    #Get detected face encoding from embedding model
    faceEncoding = face_recognition.face_encodings(image, faceLocations[0])

    #See who from database matches best
    bestMatch = recognizeFace(database, faceEncoding)

def setupDatabase():
    guests = Guest.objects.all()
    database = {}

    for guest in guests:
        textEncoding = guest.getEncoding()
        database[guest.__str__()] = np.array(textEncoding)

    return (database)

def addFace(image):
    """
    Detects and encodes faces in image
    """
    #Detect if there are any faces in the frame and get their locations
    faceLocations = hogDetectFaceLocations(image)

    #Get detected face encoding from embedding model
    faceEncoding = face_recognition.face_encodings(image, faceLocations)[0]

    return (faceEncoding)
